class ModuleDocFragment(object):
    DOCUMENTATION = r'''
options:
    elasticsearch_url:
        description:
            - The URL of the elasticsearch cluster.
            - If the value is not specified in the task, the value of environment variable C(ELASTICSEARCH_URL) will be used instead.
        required: false
        type: str
    elasticsearch_user:
        description:
            - The username for the elasticsearch cluster.
            - If the value is not specified in the task, the value of environment variable C(ELASTICSEARCH_USER) will be used instead.
        required: false
        type: str
    elasticsearch_password:
        description:
            - The password for the elasticsearch cluste.
            - If the value is not specified in the task, the value of environment variable C(ELASTICSEARCH_PASSWORD) will be used instead.
        required: false
        type: str
    elasticsearch_cert:
        description:
            - Path to the PEM encoded X.509 Cert to use as client certificate.
        required: false
        type: path
    elasticsearch_key:
        description:
            - Path to the PEM encoded client key.
        required: false
        type: path
    elasticsearch_cacert:
        description:
            - Path to the PEM encoded CA cert.
        required: false
        type: path
    validate_certs:
        description:
            - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
            - If the value is not specified in the task, the value of environment variable C(ELASTICSEARCH_VALIDATE_CERTS) will be used instead.
        required: false
        type: bool
        default: true
'''
