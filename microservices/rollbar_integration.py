import os
import rollbar

rollbar.init(
    access_token='6495d34766c549eea49fba3ba3040784',
    environment='testenv',
    code_version='1.0'
)
rollbar.report_message('Rollbar is configured correctly', 'info')
