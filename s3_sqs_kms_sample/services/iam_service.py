from aws_cdk import (
    aws_s3 as s3
    ,aws_sqs as sqs
    ,aws_kms as kms
    ,aws_iam as iam
    ,core)

class IamService:

    @staticmethod
    def create_role(self):
        
        return iam.Role(self
                        ,id='ssl-sqs-kms-role'
                        ,assumed_by=iam.CompositePrincipal(
                            iam.ServicePrincipal('s3.amazonaws.com')
                            ,iam.ServicePrincipal('sqs.amazonaws.com')
                            ,iam.ServicePrincipal('kms.amazonaws.com')
                        )
                        ,role_name='ssl-sqs-kms-role')

    @staticmethod
    def get_managed_policy(self,kms_key_arn):
        s3 = IamService.__get_s3_policy_statement(self)
        kms = IamService.__get_kms_statements(self)
        managePolicy = iam.ManagedPolicy(self
                                        ,'ssl-sqs-kms-managed-polciy'
                                        ,managed_policy_name='ssl-sqs-kms-managed-polciy'
                                        ,statements=[
                                            s3
                                            ,kms
                                        ])
        return managePolicy

    @staticmethod
    def __get_s3_policy_statement(self):
        policy_statement = iam.PolicyStatement()
        policy_statement.effect.ALLOW
        policy_statement.add_actions('s3:*')
        policy_statement.add_all_resources()
        return policy_statement

    @staticmethod
    def __get_kms_statements(self):
        policy_statement = iam.PolicyStatement()
        policy_statement.effect.ALLOW
        policy_statement.add_actions('kms:*')
        policy_statement.add_all_resources()
        return policy_statement

    @staticmethod
    def get_kms_policy_documents(self):
        policy_document = iam.PolicyDocument()
        policy_statement = iam.PolicyStatement()
        policy_statement.effect.ALLOW
        policy_statement.add_actions('kms:*')
        policy_statement.add_all_resources()
        policy_statement.add_account_root_principal()
        policy_document.add_statements(policy_statement)
        return policy_document