from enum import Enum


class AuthenticationMethodsPolicyMigrationState(Enum):
    preMigration = "0"
    migrationInProgress = "1"
    migrationComplete = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuthenticationMethodsPolicyMigrationState"
