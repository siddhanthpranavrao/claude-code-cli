from sample_app.domain.errors import TenantIsolationViolation
from sample_app.domain.models import Document, Tenant


class TenantPolicy:
    def assert_can_read(self, tenant: Tenant, document: Document) -> None:
        if tenant.id != document.tenant_id:
            raise TenantIsolationViolation("tenant isolation violated: tenant id mismatch")
        if not tenant.can_access(document.collection):
            raise TenantIsolationViolation("tenant isolation violated: collection denied")


class RetentionPolicy:
    def should_archive(self, document: Document, max_words: int = 120_000) -> bool:
        return document.word_count() > max_words or document.metadata.get("archive") is True

