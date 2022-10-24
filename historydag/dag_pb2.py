# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dag.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="dag.proto",
    package="DAG",
    syntax="proto3",
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\tdag.proto\x12\x03\x44\x41G"M\n\x03mut\x12\x10\n\x08position\x18\x01 \x01(\x05\x12\x0f\n\x07par_nuc\x18\x02 \x01(\x05\x12\x0f\n\x07mut_nuc\x18\x03 \x03(\x05\x12\x12\n\nchromosome\x18\x05 \x01(\t"\x8d\x01\n\x04\x65\x64ge\x12\x0f\n\x07\x65\x64ge_id\x18\x01 \x01(\x03\x12\x13\n\x0bparent_node\x18\x02 \x01(\x03\x12\x14\n\x0cparent_clade\x18\x03 \x01(\x03\x12\x12\n\nchild_node\x18\x04 \x01(\x03\x12 \n\x0e\x65\x64ge_mutations\x18\x05 \x03(\x0b\x32\x08.DAG.mut\x12\x13\n\x0b\x65\x64ge_weight\x18\x06 \x01(\x02"6\n\tnode_name\x12\x0f\n\x07node_id\x18\x01 \x01(\x03\x12\x18\n\x10\x63ondensed_leaves\x18\x02 \x03(\t"q\n\x04\x64\x61ta\x12\x18\n\x05\x65\x64ges\x18\x01 \x03(\x0b\x32\t.DAG.edge\x12"\n\nnode_names\x18\x02 \x03(\x0b\x32\x0e.DAG.node_name\x12\x14\n\x0creference_id\x18\x03 \x01(\t\x12\x15\n\rreference_seq\x18\x04 \x01(\tb\x06proto3', # noqa
)


_MUT = _descriptor.Descriptor(
    name="mut",
    full_name="DAG.mut",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="position",
            full_name="DAG.mut.position",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="par_nuc",
            full_name="DAG.mut.par_nuc",
            index=1,
            number=2,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="mut_nuc",
            full_name="DAG.mut.mut_nuc",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="chromosome",
            full_name="DAG.mut.chromosome",
            index=3,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=18,
    serialized_end=95,
)


_EDGE = _descriptor.Descriptor(
    name="edge",
    full_name="DAG.edge",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="edge_id",
            full_name="DAG.edge.edge_id",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="parent_node",
            full_name="DAG.edge.parent_node",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="parent_clade",
            full_name="DAG.edge.parent_clade",
            index=2,
            number=3,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="child_node",
            full_name="DAG.edge.child_node",
            index=3,
            number=4,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="edge_mutations",
            full_name="DAG.edge.edge_mutations",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="edge_weight",
            full_name="DAG.edge.edge_weight",
            index=5,
            number=6,
            type=2,
            cpp_type=6,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=98,
    serialized_end=239,
)


_NODE_NAME = _descriptor.Descriptor(
    name="node_name",
    full_name="DAG.node_name",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="node_id",
            full_name="DAG.node_name.node_id",
            index=0,
            number=1,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="condensed_leaves",
            full_name="DAG.node_name.condensed_leaves",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=241,
    serialized_end=295,
)


_DATA = _descriptor.Descriptor(
    name="data",
    full_name="DAG.data",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="edges",
            full_name="DAG.data.edges",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="node_names",
            full_name="DAG.data.node_names",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="reference_id",
            full_name="DAG.data.reference_id",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="reference_seq",
            full_name="DAG.data.reference_seq",
            index=3,
            number=4,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=297,
    serialized_end=410,
)

_EDGE.fields_by_name["edge_mutations"].message_type = _MUT
_DATA.fields_by_name["edges"].message_type = _EDGE
_DATA.fields_by_name["node_names"].message_type = _NODE_NAME
DESCRIPTOR.message_types_by_name["mut"] = _MUT
DESCRIPTOR.message_types_by_name["edge"] = _EDGE
DESCRIPTOR.message_types_by_name["node_name"] = _NODE_NAME
DESCRIPTOR.message_types_by_name["data"] = _DATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

mut = _reflection.GeneratedProtocolMessageType(
    "mut",
    (_message.Message,),
    {
        "DESCRIPTOR": _MUT,
        "__module__": "dag_pb2"
        # @@protoc_insertion_point(class_scope:DAG.mut)
    },
)
_sym_db.RegisterMessage(mut)

edge = _reflection.GeneratedProtocolMessageType(
    "edge",
    (_message.Message,),
    {
        "DESCRIPTOR": _EDGE,
        "__module__": "dag_pb2"
        # @@protoc_insertion_point(class_scope:DAG.edge)
    },
)
_sym_db.RegisterMessage(edge)

node_name = _reflection.GeneratedProtocolMessageType(
    "node_name",
    (_message.Message,),
    {
        "DESCRIPTOR": _NODE_NAME,
        "__module__": "dag_pb2"
        # @@protoc_insertion_point(class_scope:DAG.node_name)
    },
)
_sym_db.RegisterMessage(node_name)

data = _reflection.GeneratedProtocolMessageType(
    "data",
    (_message.Message,),
    {
        "DESCRIPTOR": _DATA,
        "__module__": "dag_pb2"
        # @@protoc_insertion_point(class_scope:DAG.data)
    },
)
_sym_db.RegisterMessage(data)


# @@protoc_insertion_point(module_scope)
