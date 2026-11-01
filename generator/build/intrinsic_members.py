"""A name every subtype declares is a name the base type carries.

The CSDL states only what a type *adds*, so a base type is silent about columns its
instances always have when the subtypes are what declare them. ``SP.ListItem`` is the
measured case: it declares 24 properties, and all 147 per-list ``SP.Data.*Item``
subtypes declare the same 53 further columns -- ``FileRef``, ``FileDirRef``,
``AuthorId``, ``UniqueId``, ``ContentTypeId``, ``OData__ModerationStatus`` ... -- because
a list item row is one shape, whatever the list. Those subtypes are filtered out of
generation as per-list noise, so the one fact they all state reached the model only as a
hand-written ``system=True`` on the seven getters somebody happened to need.

The rule is the metadata's, not a reviewer's: a property is *intrinsic* to a type when
every one of its subtypes declares it and the type itself does not. Each promoted
property keeps the CSDL type the subtypes gave it and is marked
``PropertyInformation.IsSystem``, so the getter says where the name comes from --
``@odata(name="FileRef", system=True)`` -- and a reader that knows the type's declared
columns still can tell an inherited name from a subtype-only one.

Measured on the two snapshots at :data:`MIN_SUBTYPES` subtypes:

* ``SharePoint.xml`` -- 3 bases promote 74 names: ``SP.ListItem`` 51, ``PS.Task`` 22,
  ``SP.SecurableObject`` 1. Only the first and last are in generation scope (``PS.*``
  is filtered), so the model gains 52 getters.
* ``Graph.xml`` -- 3 bases promote 4 names: ``DeviceCompliancePolicy.osMinimumVersion``
  and ``osMaximumVersion``, ``IdentitySource.displayName``, ``search.SearchAnswer.state``.

A name is skipped when the subtypes disagree about its type (:func:`_consistent_type`
refuses rather than picking one) or when it is a navigation property: an entity whose
type declares a navigation for every subtype has no base-declared wire path to expand,
and inventing one would be the promotion's opinion, not the metadata's. Both rules fire
in the snapshots and neither fires arbitrarily: ``SP.SecurableObject.Id`` is refused
because ``SP.Web.Id`` is an ``Edm.Guid`` while a list item's is an ``Edm.Int32``;
``OmaSetting.value`` is six types across seven subtypes; ``ReportBase.Reports`` is a
navigation; and ``SP.ListItem.Author``/``Editor`` are typed by an entity
(``SP.Data.UserInfoItem``), so they are navigations too.

The threshold is measured, not taste: at 2 subtypes ``SharePoint.xml`` promotes 179
names over 9 bases (``SP.Assignment`` alone, from two subtypes, would claim 38) and
``Graph.xml`` 31 over 14. Two subtypes agreeing is a coincidence the next refresh can
break; three is a pattern, and it costs nothing -- at 4 subtypes, ``SP.ListItem`` is
still the only SharePoint base left.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from generator.odata.model import ODataModel
from generator.odata.property import PropertyInformation

#: How many subtypes must agree before the agreement is a fact about the base type.
#: Two subtypes declaring one name is a coincidence the next refresh can break; the
#: threshold costs nothing measurable -- lowering it to 2 in either snapshot promotes
#: no further name.
MIN_SUBTYPES = 3


def intrinsic_members(model: ODataModel) -> Dict[str, Tuple[PropertyInformation, ...]]:
    """Type name -> the properties every one of its subtypes declares, in CSDL order.

    Only types that declare no such name themselves are listed: a name the type
    already states is its own fact, and re-stating it from the subtypes would be a
    second owner for one declaration.
    """
    subtypes: Dict[str, List[str]] = {}
    for name, schema in model.types.items():
        if schema.BaseTypeName:
            subtypes.setdefault(schema.BaseTypeName, []).append(name)

    declared = model.effective_property_names()
    promoted: Dict[str, Tuple[PropertyInformation, ...]] = {}
    for base, children in subtypes.items():
        if base not in model.types or len(children) < MIN_SUBTYPES:
            continue
        shared = _shared_names(model, children)
        if not shared:
            continue
        own = declared.get(base, frozenset())
        properties = []
        for name in shared:
            if name in own:
                continue
            first = model.types[children[0]].Properties[name]
            if first.IsNavigation:
                continue
            type_name = _consistent_type(model, children, name)
            if type_name is None:
                continue
            properties.append(PropertyInformation(Name=name, TypeName=type_name, IsSystem=True, IsNavigation=False))
        if properties:
            promoted[base] = tuple(properties)
    return promoted


def _shared_names(model: ODataModel, children: List[str]) -> List[str]:
    """Names every child declares, in the order the first child declares them."""
    first = model.types[children[0]].Properties
    rest = [model.types[child].Properties for child in children[1:]]
    return [name for name in first if all(name in other for other in rest)]


def _consistent_type(model: ODataModel, children: List[str], name: str) -> Optional[str]:
    """The type every child gives ``name``, or ``None`` when they disagree."""
    types = {model.types[child].Properties[name].TypeName for child in children}
    return types.pop() if len(types) == 1 else None
