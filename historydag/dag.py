import ete3
import pickle
import graphviz as gv
import random
from Bio.Data.IUPACData import ambiguous_dna_values
from collections import Counter
from gctree.utils import hamming_distance


def product(optionlist, accum=tuple()):
    """Takes a list of functions which each return a fresh generator
    on options at that site"""
    if optionlist:
        for term in optionlist[0]():
            yield from product(optionlist[1:], accum=(accum + (term,)))
    else:
        yield accum


class SdagNode:
    """A recursive representation of an sDAG
    - a dictionary keyed by clades (frozensets) containing EdgeSet objects
    - a label
    """

    def __init__(self, label, clades: dict = {}):
        self.clades = clades
        # If passed a nonempty dictionary, need to add self to children's parents
        self.label = label
        self.parents = set()
        if self.clades:
            for _, edgeset in self.clades.items():
                edgeset.parent = self
            for child in self.children():
                child.parents.add(self)

    def __repr__(self):
        return str((self.label, set(self.clades.keys())))

    def __hash__(self):
        return hash((self.label, frozenset(self.clades.keys())))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def node_self(self):
        return SdagNode(self.label, {clade: EdgeSet() for clade in self.clades})

    def under_clade(self):
        """Returns the union of all child clades"""
        if self.is_leaf():
            return(frozenset([self.label]))
        else:
            return(frozenset().union(*self.clades.keys()))

    def copy(self):
        """Add each child node's copy, below this node, by merging"""
        newnode = self.node_self()
        from_root = newnode.label == "DAG_root"
        for clade in self.clades:
            for index, target in enumerate(self.clades[clade].targets):
                othernode = self.node_self()
                othernode.clades[clade].add_to_edgeset(target.copy(), from_root=from_root)
                newnode.merge(othernode)
                newnode.clades[clade].weights[index] = self.clades[clade].weights[index]
                newnode.clades[clade].probs[index] = self.clades[clade].probs[index]
        return newnode

    def merge(self, node):
        """performs post order traversal to add node and all of its children,
        without introducing duplicate nodes in self. Requires given node is a root"""
        if not hash(self) == hash(node):
            raise ValueError(
                f"The given node must be a root node on identical taxa.\n{self}\nvs\n{node}"
            )
        selforder = postorder(self)
        nodeorder = postorder(node)
        hashdict = {hash(n): n for n in selforder}
        for n in nodeorder:
            if hash(n) in hashdict:
                pnode = hashdict[hash(n)]
            else:
                pnode = n.node_self()
                hashdict[hash(n)] = pnode

            for _, edgeset in n.clades.items():
                for child, weight, _ in edgeset:
                    pnode.add_edge(hashdict[hash(child)], weight=weight)

    def add_edge(self, target, weight=0, prob=None, prob_norm=True):
        """Adds edge, if not already present and allowed. Returns if edge was added."""
        # target clades must union to a clade of self
        key = target.under_clade()
        if key not in self.clades:
            print(key)
            print(self.clades)
            raise KeyError("Target clades' union is not a clade of this parent node")
        else:
            from_root = self.label == "DAG_root"
            target.parents.add(self)
            return self.clades[key].add_to_edgeset(target, weight=weight, prob=prob, prob_norm=prob_norm, from_root=from_root)

    def is_leaf(self):
        return not bool(self.clades)

    def partitions(self):
        return self.clades.keys()

    def children(self, clade=None):
        """If clade is provided, returns generator object of edge targets from that
        clade. If no clade is provided, generator includes all children of self.
        """
        if clade is None:
            return (
                target for clade in self.clades for target, _, _ in self.clades[clade]
            )
        else:
            return (child for child, _, _ in self.clades[clade])

    def add_all_allowed_edges(self):
        n_added = 0
        clade_dict = {node.under_clade(): [] for node in postorder(self)}
        for node in postorder(self):
            clade_dict[node.under_clade()].append(node)
        for node in postorder(self):
            for clade in node.clades:
                for target in clade_dict[clade]:
                    n_added += node.add_edge(target)
        return(n_added)

    def to_newick(self, namedict={}):
        """Converts to extended newick format with arbitrary node names and a
        sequence feature. For use on tree-shaped DAG"""

        def newick(node):
            if node.label in namedict:
                name = namedict[node.label]
            else:
                name = "1"
            if node.is_leaf():
                return f"{name}[&&NHX:sequence={node.label}]"
            else:
                return (
                    "("
                    + ",".join([newick(node2) for node2 in node.children()])
                    + ")"
                    + f"{name}[&&NHX:sequence={node.label}]"
                )

        if self.label == "DAG_root":
            return newick(next(self.children())) + ";"
        else:
            return newick(self) + ";"

    def to_ete(self, namedict={}):
        return ete3.TreeNode(newick=self.to_newick(namedict=namedict), format=1)

    def to_graphviz(self, namedict={}, show_partitions=True):
        """Converts to graphviz Digraph object. Namedict must associate sequences
        of all leaf nodes to a name
        """

        def taxa(clade):
            l = [labeller(taxon) for taxon in clade]
            l.sort()
            return ",".join(l)

        def min_weight_under(node):
            try:
                return node.min_weight_under
            except:
                return ""

        def labeller(sequence):
            if len(sequence) < 11:
                return sequence
            elif sequence in namedict:
                return str(namedict[sequence])
            else:
                return hash(sequence)

        G = gv.Digraph("labeled partition DAG", node_attr={"shape": "record"})
        for node in postorder(self):
            if node.is_leaf() or show_partitions is False:
                G.node(str(id(node)), f"<label> {labeller(node.label)}")
            else:
                splits = "|".join(
                    [f"<{taxa(clade)}> {taxa(clade)}" for clade in node.clades]
                )
                G.node(
                    str(id(node)), f"{{ <label> {labeller(node.label)} |{{{splits}}} }}"
                )
            for clade in node.clades:
                for target, weight, prob in node.clades[clade]:
                    label = ""
                    if prob < 1.0:
                        label += f"p:{prob:.2f}"
                    if weight > 0.0:
                        label += f"w:{weight}"
                    G.edge(
                        f"{id(node)}:{taxa(clade) if show_partitions else 'label'}",
                        f"{id(target)}:label",
                        label=label,
                    )
        return G

    def weight(self):
        "Sums weights of all edges in the DAG"
        nodes = postorder(self)
        edgesetsums = (
            sum(edgeset.weights) for node in nodes for edgeset in node.clades.values()
        )
        return sum(edgesetsums)

    def internal_avg_parents(self):
        """Returns the average number of parents among internal nodes
        A simple measure of similarity of trees that the DAG expresses."""
        nonleaf_parents = (len(n.parents) for n in postorder(self) if not n.is_leaf())
        n = 0
        cumsum = 0
        for sum in nonleaf_parents:
            n += 1
            cumsum += sum
        # Exclude root:
        return cumsum / float(n - 1)

    def sample(self, min_weight=False):
        """Samples a sub-history-DAG that is also a tree containing the root and
        all leaf nodes. Returns a new SdagNode object"""
        sample = self.node_self()
        from_root = sample.label == "DAG_root"
        for clade, eset in self.clades.items():
            sampled_target, target_weight = eset.sample(min_weight=min_weight)
            sample.clades[clade].add_to_edgeset(
                sampled_target.sample(min_weight=min_weight), weight=target_weight,
                from_root=from_root
            )
        return sample

    def count_trees(self, min_weight=False):
        """Annotates each node in the DAG with the number of complete trees underneath (extending to leaves,
        and containing exactly one edge for each node-clade pair). Returns the total number of unique
        complete trees below the root node."""
        # Replace prod function later:
        prod = lambda l: l[0] * prod(l[1:]) if l else 1
        # logic below requires prod([]) == 1!!
        for node in postorder(self):
            node.trees_under = prod(
                [
                    sum([target.trees_under for target in node.clades[clade].targets])
                    for clade in node.clades
                ]
            )
        return self.trees_under

    def get_trees(self, min_weight=False):
        """Return a generator to iterate through all trees expressed by the DAG."""

        if min_weight:
            dag = self.prune_min_weight()
        else:
            dag = self

        def genexp_func(clade):
            # Return generator expression of all possible choices of tree
            # structure from dag below clade
            def f():
                eset = self.clades[clade]
                return (
                    (clade, targettree, i)
                    for i, target in enumerate(eset.targets)
                    for targettree in target.get_trees(min_weight=min_weight)
                )

            return f

        optionlist = [genexp_func(clade) for clade in self.clades]

        for option in product(optionlist):
            tree = dag.node_self()
            from_root = tree.label == "DAG_root"
            for clade, targettree, index in option:
                tree.clades[clade].add_to_edgeset(
                    targettree, weight=dag.clades[clade].weights[index],
                    from_root=from_root
                )
            yield tree

    def min_weight_annotate(self):
        for node in postorder(self):
            if node.is_leaf():
                node.min_weight_under = 0
            else:
                min_sum = sum(
                    [
                        min(
                            [
                                child.min_weight_under
                                + dag_hamming_distance(child.label, node.label)
                                for child in node.clades[clade].targets
                            ]
                        )
                        for clade in node.clades
                    ]
                )
                node.min_weight_under = min_sum
        return self.min_weight_under

    def get_weight_counts(self):
        # Replace prod function later

        prod = lambda l: l[0] * prod(l[1:]) if l else 1

        def counter_prod(counterlist):
            newc = Counter()
            for combi in product([c.items for c in counterlist]):
                weights, counts = [[t[i] for t in combi] for i in range(len(combi[0]))]
                newc.update({sum(weights): prod(counts)})
            return newc

        def counter_sum(counterlist):
            newc = Counter()
            for c in counterlist:
                newc += c
            return newc

        def addweight(c, w):
            return Counter({key + w: val for key, val in c.items()})

        for node in postorder(self):
            if node.is_leaf():
                node.weight_counter = Counter({0: 1})
            else:
                cladelists = [
                    [
                        addweight(
                            target.weight_counter,
                            dag_hamming_distance(target.label, node.label),
                        )
                        for target in node.clades[clade].targets
                    ]
                    for clade in node.clades
                ]
                cladecounters = [counter_sum(cladelist) for cladelist in cladelists]
                node.weight_counter = counter_prod(cladecounters)
        return self.weight_counter

    def prune_min_weight(self):
        newdag = self.copy()
        newdag.min_weight_annotate()
        # It may not be okay to use preorder here. May need reverse postorder
        # instead?
        for node in preorder(newdag):
            for clade, eset in node.clades.items():
                weightlist = [
                    (
                        target.min_weight_under
                        + dag_hamming_distance(target.label, node.label),
                        target,
                        index,
                    )
                    for index, target in enumerate(eset.targets)
                ]
                minweight = min([weight for weight, _, _ in weightlist])
                newtargets = []
                newweights = []
                for weight, target, index in weightlist:
                    if weight == minweight:
                        newtargets.append(target)
                        newweights.append(eset.weights[index])
                eset.targets = newtargets
                eset.weights = newweights
                n = len(eset.targets)
                eset.probs = [1.0 / n] * n
        return newdag

    def serialize(self):
        """Represents SdagNode object as a list of sequences, a list of node tuples containing
        (node sequence index, frozenset of frozenset of leaf sequence indices)
        and an edge list containing a tuple for each edge:
        (origin node index, target node index, edge weight, edge probability)"""
        sequence_list = []
        node_list = []
        edge_list = []
        sequence_indices = {}
        node_indices = {id(node): idx for idx, node in enumerate(postorder(self))}

        def cladesets(node):
            clades = {
                frozenset({sequence_indices[sequence] for sequence in clade})
                for clade in node.clades
            }
            return frozenset(clades)

        for node in postorder(self):
            if node.label not in sequence_indices:
                sequence_indices[node.label] = len(sequence_list)
                sequence_list.append(node.label)
                assert sequence_list[sequence_indices[node.label]] == node.label
            node_list.append((sequence_indices[node.label], cladesets(node)))
            node_idx = len(node_list) - 1
            for eset in node.clades.values():
                for idx, target in enumerate(eset.targets):
                    edge_list.append(
                        (
                            node_idx,
                            node_indices[id(target)],
                            eset.weights[idx],
                            eset.probs[idx],
                        )
                    )
        serial_dict = {
            "sequence_list": sequence_list,
            "node_list": node_list,
            "edge_list": edge_list,
        }
        return pickle.dumps(serial_dict)


class EdgeSet:
    """Goal: associate targets (edges) with arbitrary parameters, but support
    set-like operations like lookup and enforce that elements are unique."""

    def __init__(self, *args, weights: list = None, probs: list = None):
        """Takes no arguments, or an ordered iterable containing target nodes"""
        if len(args) > 1:
            raise TypeError(f"Expected at most one argument, got {len(args)}")
        elif args:
            self.targets = list(args[0])
            n = len(self.targets)
            if weights is not None:
                self.weights = weights
            else:
                self.weights = [0] * n

            if probs is not None:
                self.probs = probs
            else:
                self.probs = [float(1) / n] * n
        else:
            self.targets = []
            self.weights = []
            self.probs = []
            self._hashes = set()

        self._hashes = {hash(self.targets[i]) for i in range(len(self.targets))}
        if not len(self._hashes) == len(self.targets):
            raise TypeError("First argument may not contain duplicate target nodes")
        # Should probably also check to see that all passed lists have same length

    def __iter__(self):
        return (
            (self.targets[i], self.weights[i], self.probs[i])
            for i in range(len(self.targets))
        )

    def copy(self):
        return EdgeSet(
            [node.copy() for node in self.targets],
            weights=self.weights.copy(),
            probs=self.probs.copy(),
        )

    def sample(self, min_weight=False):
        """Returns a randomly sampled child edge, and the corresponding entry from the
        weight vector. If min_weight is True, samples only target nodes with lowest
        min_weight_under attribute, ignoring edge probabilities."""
        if min_weight:
            mw = min(
                node.min_weight_under
                + dag_hamming_distance(self.parent.label, node.label)
                for node in self.targets
            )
            options = [
                i
                for i, node in enumerate(self.targets)
                if (
                    node.min_weight_under
                    + dag_hamming_distance(self.parent.label, node.label)
                )
                == mw
            ]
            index = random.choices(options, k=1)[0]
            return (self.targets[index], self.weights[index])
        else:
            index = random.choices(
                list(range(len(self.targets))), weights=self.probs, k=1
            )[0]
            return (self.targets[index], self.weights[index])

    def add_to_edgeset(self, target, weight=0, prob=None, prob_norm=True, from_root=False):
        """currently does nothing if edge is already present. Also does nothing
        if the target node has one child clade, and parent node is not the DAG root.
        Returns whether an edge was added""" 
        if target.label == "DAG_root":
            return False
        elif hash(target) in self._hashes:
            return False
        elif not from_root and len(target.clades) == 1:
            return False
        else:
            self._hashes.add(hash(target))
            self.targets.append(target)
            self.weights.append(weight)

            if prob is None:
                prob = 1.0 / len(self.targets)
            if prob_norm:
                self.probs = list(
                    map(lambda x: x * (1 - prob) / sum(self.probs), self.probs)
                )
            self.probs.append(prob)
            return True


def from_tree(tree: ete3.TreeNode):
    def leaf_names(r: ete3.TreeNode):
        return frozenset((node.sequence for node in r.get_leaves()))

    def _unrooted_from_tree(tree):
        dag = SdagNode(
            tree.sequence,
            {
                leaf_names(child): EdgeSet(
                    [_unrooted_from_tree(child)], weights=[child.dist]
                )
                for child in tree.get_children()
            },
        )
        return dag

    dag = _unrooted_from_tree(tree)
    dagroot = SdagNode(
        "DAG_root",
        {
            frozenset({taxon for s in dag.clades for taxon in s}): EdgeSet(
                [dag], weights=[tree.dist]
            )
        },
    )
    dagroot.add_edge(dag, weight=0)
    return dagroot


def from_newick(tree: str):
    etetree = ete3.Tree(tree, format=8)
    return from_tree(etetree)


def postorder(dag: SdagNode):
    visited = set()

    def traverse(node: SdagNode):
        visited.add(id(node))
        if not node.is_leaf():
            for child in node.children():
                if not id(child) in visited:
                    yield from traverse(child)
        yield node

    yield from traverse(dag)


def preorder(dag: SdagNode):
    """Careful! remember this is not guaranteed to visit a parent node before any of its children.
    for that, need reverse postorder traversal."""
    visited = set()

    def traverse(node: SdagNode):
        visited.add(id(node))
        yield node
        if not node.is_leaf():
            for child in node.children():
                if not id(child) in visited:
                    yield from traverse(child)

    yield from traverse(dag)


def sdag_from_newicks(newicklist):
    treelist = list(map(lambda x: ete3.Tree(x, format=8), newicklist))
    for tree in treelist:
        for node in tree.traverse():
            node.sequence = node.name
    return sdag_from_etes(treelist)


def sdag_from_etes(treelist):
    dag = from_tree(treelist[0])
    for tree in treelist[1:]:
        dag.merge(from_tree(tree))
    return dag


def disambiguate(tree: ete3.TreeNode, random_state=None) -> ete3.TreeNode:
    """Resolve tree and return list of all possible resolutions"""
    bases = "AGCT-"
    ambiguous_dna_values.update({"?": "GATC-", "-": "-"})
    code_vectors = {
        code: [
            0 if base in ambiguous_dna_values[code] else float("inf") for base in bases
        ]
        for code in ambiguous_dna_values
    }
    cost_adjust = {
        base: [int(not i == j) for j in range(5)] for i, base in enumerate(bases)
    }
    if random_state is None:
        random.seed(tree.write(format=1))
    else:
        random.setstate(random_state)

    for node in tree.traverse(strategy="postorder"):

        def cvup(node, site):
            cv = code_vectors[node.sequence[site]].copy()
            if not node.is_leaf():
                for i in range(5):
                    for child in node.children:
                        cv[i] += min(
                            [
                                sum(v)
                                for v in zip(child.cvd[site], cost_adjust[bases[i]])
                            ]
                        )
            return cv

        # Make dictionary of cost vectors for each site
        node.cvd = {site: cvup(node, site) for site in range(len(node.sequence))}

    disambiguated = [tree.copy()]
    ambiguous = True
    while ambiguous:
        ambiguous = False
        treesindex = 0
        while treesindex < len(disambiguated):
            tree2 = disambiguated[treesindex]
            treesindex += 1
            for node in tree2.traverse(strategy="preorder"):
                ambiguous_sites = [
                    site for site, code in enumerate(node.sequence) if code not in bases
                ]
                if not ambiguous_sites:
                    continue
                else:
                    ambiguous = True
                    # Adjust cost vectors for ambiguous sites base on above
                    if not node.is_root():
                        for site in ambiguous_sites:
                            base_above = node.up.sequence[site]
                            node.cvd[site] = [
                                sum(v)
                                for v in zip(node.cvd[site], cost_adjust[base_above])
                            ]
                    option_dict = {site: "" for site in ambiguous_sites}
                    # Enumerate min-cost choices
                    for site in ambiguous_sites:
                        min_cost = min(node.cvd[site])
                        min_cost_sites = [
                            bases[i]
                            for i, val in enumerate(node.cvd[site])
                            if val == min_cost
                        ]
                        option_dict[site] = "".join(min_cost_sites)

                    def _options(option_dict, sequence):
                        if option_dict:
                            site, choices = option_dict.popitem()
                            for choice in choices:
                                sequence = (
                                    sequence[:site] + choice + sequence[site + 1 :]
                                )
                                yield from _options(option_dict.copy(), sequence)
                        else:
                            yield sequence

                    sequences = list(_options(option_dict, node.sequence))
                    # Give this tree the first sequence, append copies with all
                    # others to disambiguated.
                    numseqs = len(sequences)
                    for idx, sequence in enumerate(sequences):
                        node.sequence = sequence
                        if idx < numseqs - 1:
                            disambiguated.append(tree2.copy())
                    break
    for tree in disambiguated:
        for node in tree.traverse():
            try:
                node.del_feature("cvd")
            except KeyError:
                pass
    return disambiguated


def dag_analysis(in_trees, n_samples=100):
    in_tree_weights = [recalculate_ete_parsimony(tree) for tree in in_trees]
    print("Input trees have the following weight distribution:")
    hist(Counter(in_tree_weights), samples=len(in_tree_weights))
    resolvedset = {from_tree(tree).to_newick() for tree in in_trees}
    print(len(resolvedset), " unique input trees")
    dag = sdag_from_etes(in_trees)

    dagsamples = []
    for _ in range(n_samples):
        dagsamples.append(dag.sample())
    dagsampleweights = [sample.weight() for sample in dagsamples]
    sampleset = {tree.to_newick() for tree in dagsamples}
    print("\nSampled trees have the following weight distribution:")
    hist(Counter(dagsampleweights), samples=n_samples)
    print(len(sampleset), " unique sampled trees")
    print(len(sampleset - resolvedset), " sampled trees were not DAG inputs")


def disambiguate_all(treelist):
    resolvedsamples = []
    for sample in treelist:
        resolvedsamples.extend(disambiguate(sample))
    return resolvedsamples


def dag_hamming_distance(s1, s2):
    if s1 == "DAG_root" or s2 == "DAG_root":
        return 0
    else:
        return hamming_distance(s1, s2)


def recalculate_ete_parsimony(tree: ete3.TreeNode) -> float:
    tree.dist = 0
    for node in tree.iter_descendants():
        node.dist = hamming_distance(node.sequence, node.up.sequence)
    return total_weight(tree)


def recalculate_parsimony(tree: SdagNode):
    for node in postorder(tree):
        for clade, eset in node.clades.items():
            for i in range(len(eset.targets)):
                eset.weights[i] = dag_hamming_distance(
                    eset.targets[i].label, node.label
                )
    return tree.weight()


def hist(c: Counter, samples=1):
    l = list(c.items())
    l.sort()
    print("Weight | Frequency", "\n------------------")
    for weight, freq in l:
        print(f"{weight}   | {freq/samples}")


def total_weight(tree: ete3.TreeNode) -> float:
    return sum(node.dist for node in tree.traverse())


def deserialize(bstring):
    """reloads an SdagNode serialized object, as ouput by SdagNode.serialize"""
    serial_dict = pickle.loads(bstring)
    sequence_list = serial_dict["sequence_list"]
    node_list = serial_dict["node_list"]
    edge_list = serial_dict["edge_list"]

    def unpack_seqs(seqset):
        return frozenset({sequence_list[idx] for idx in seqset})

    node_postorder = [
        SdagNode(
            sequence_list[idx], {unpack_seqs(clade): EdgeSet() for clade in clades}
        )
        for idx, clades in node_list
    ]
    # Last node in list is root
    for origin_idx, target_idx, weight, prob in edge_list:
        node_postorder[origin_idx].add_edge(
            node_postorder[target_idx], weight=weight, prob=prob, prob_norm=False
        )
    return node_postorder[-1]
