from .models import AuditLog


def create_audit_log(user, organization, action, team= None, metadata=None, request=None):
    ip = request.Meta.get('REMOTE_ADDR') if request else None

    return AuditLog.objects.create(
        actor = user,
        organization = organization,
        team=team,
        action=action,
        metadata = metadata or {},
        ip_address = ip
    )