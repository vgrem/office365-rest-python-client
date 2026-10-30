"""Offline tests for OData return-type classification and rendering (codegen side)."""

from __future__ import annotations

from generator.builders.references import ReturnType, TypeKind
from generator.builders.resolution import TypeRegistry


def _resolver() -> TypeRegistry:
    return TypeRegistry(["office365.sharepoint"])


def test_void_type():
    return_type = ReturnType(None)
    assert return_type.kind is TypeKind.VOID
    assert return_type.is_void is True


def test_primitive_and_stream():
    primitive = ReturnType("Edm.Int32")
    assert primitive.kind is TypeKind.PRIMITIVE
    assert primitive.annotation == "ClientResult[int]"
    assert primitive.default("self.context") == "ClientResult(self.context, int())"

    stream = ReturnType("Edm.Stream")
    assert stream.is_stream is True
    assert stream.annotation == "ClientResult[bytes]"
    assert stream.default("context") == "ClientResult(context, bytes())"


def test_time_primitive():
    time_type = ReturnType("Edm.Time")
    assert time_type.kind is TypeKind.PRIMITIVE
    assert time_type.annotation == "ClientResult[time]"
    assert time_type.default("self.context") == "ClientResult(self.context, time.min)"


def test_guid_primitive_default_uses_imported_uuid():
    guid = ReturnType("Edm.Guid")
    assert guid.kind is TypeKind.PRIMITIVE
    assert guid.annotation == "ClientResult[UUID]"
    assert guid.default("context") == "ClientResult(context, UUID(int=0))"


def test_entity_and_client_value():
    entity = ReturnType("SP.Web", _resolver())
    assert entity.kind is TypeKind.ENTITY
    assert entity.annotation == "Web"
    assert entity.default("self.context") == "Web(self.context)"

    client_value = ReturnType("SP.Utilities.LLMColumnInfo", _resolver())
    assert client_value.kind is TypeKind.CLIENT_VALUE
    assert client_value.annotation == "ClientResult[LLMColumnInfo]"
    assert client_value.default("self.context") == "ClientResult(self.context, LLMColumnInfo())"


def test_a_client_value_the_run_writes_is_classified_before_it_can_be_imported():
    """A complex type written by this run has no module to inspect yet."""
    name = "Microsoft.Online.SharePoint.TenantAdministration.SPORestrictedAppAccessControlSitePolicy"
    return_type = ReturnType(name, _resolver(), frozenset({name}))

    assert return_type.kind is TypeKind.CLIENT_VALUE
    assert return_type.annotation == "ClientResult[SPORestrictedAppAccessControlSitePolicy]"
    assert return_type.default("self.context") == (
        "ClientResult(self.context, SPORestrictedAppAccessControlSitePolicy())"
    )


def test_the_metadata_name_is_matched_the_way_the_model_keys_it():
    """The CSDL spells the last segment in lower case; the model Pascal-cases it."""
    return_type = ReturnType("SP.Comments.comment", None, frozenset({"SP.Comments.Comment"}))

    assert return_type.kind is TypeKind.CLIENT_VALUE
    assert return_type.default("context") == "ClientResult(context, Comment())"


def test_primitive_collections():
    strings = ReturnType("Collection(Edm.String)")
    assert strings.kind is TypeKind.PRIMITIVE_COLLECTION
    assert strings.annotation == "ClientResult[StringCollection]"
    assert strings.default("self.context") == "ClientResult(self.context, StringCollection())"

    ints = ReturnType("Collection(Edm.Int32)")
    assert ints.annotation == "ClientResult[ClientValueCollection[int]]"
    assert ints.default("self.context") == "ClientResult(self.context, ClientValueCollection(int))"

    key_values = ReturnType("Collection(SP.KeyValue)")
    assert key_values.annotation == "ClientResult[dict]"
    assert key_values.default("self.context") == "ClientResult(self.context, dict())"


def test_entity_and_client_value_collections():
    entities = ReturnType("Collection(SP.Web)", _resolver())
    assert entities.kind is TypeKind.ENTITY_COLLECTION
    assert entities.annotation == "EntityCollection[Web]"
    assert entities.default("self.context") == "EntityCollection(self.context, Web)"

    client_values = ReturnType("Collection(SP.Compliance.Tags.ComplianceTag)", _resolver())
    assert client_values.kind is TypeKind.CLIENT_VALUE_COLLECTION
    assert client_values.annotation == "ClientResult[ClientValueCollection[ComplianceTag]]"
    assert client_values.default("self.context") == "ClientResult(self.context, ClientValueCollection[ComplianceTag]())"
