#!GET-request https://api.uomg.com/api/icp 'domain={{ __property.request.params.domain }}'

## 当前域名备案状态

当前状态：{{ __data.code }}

当前域名：{{ __data.domain }}

备注状态：{{ __data.icp }}
