from sample_app.domain.errors import TenantIsolationViolation


def require_tenant_header(headers: dict[str, str]) -> str:
    tenant_id = headers.get("x-tenant-id")
    if not tenant_id:
        raise TenantIsolationViolation("tenant isolation requires x-tenant-id header")
    return tenant_id

