from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from extensions import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    provider = Column(Enum('aws','azure','gcp', name='provider_enum'), nullable=False)
    auth_type = Column(Enum('access_key','iam_role','service_principal','service_account', name='auth_type_enum'), nullable=False)

    # AWS-specific
    access_key = Column(String(256), nullable=True)
    secret_key = Column(String(256), nullable=True)
    role_arn = Column(String(256), nullable=True)
    external_id = Column(String(256), nullable=True)

    # Azure-specific
    subscription_id = Column(String(64), nullable=True)
    tenant_id = Column(String(64), nullable=True)
    client_id = Column(String(64), nullable=True)
    client_secret = Column(String(256), nullable=True)

    # GCP-specific
    service_account_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'authType': self.auth_type,
            'accessKey': self.access_key,
            'roleArn': self.role_arn,
            'externalId': self.external_id,
            'subscriptionId': self.subscription_id,
            'tenantId': self.tenant_id,
            'clientId': self.client_id,
            'serviceAccountJson': self.service_account_json,
            'createdAt': self.created_at.isoformat()
        }
