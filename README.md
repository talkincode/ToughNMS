# ToughNMS

一个基于Python+Nagios+mongodb实现的监控管理应用



## nagios 配置

### perfdata

    # 'process-host-perfdata' command definition
    define command{
            command_name    process-host-perfdata
            command_line    curl -d "l=$LASTHOSTCHECK$&c=$SERVICECHECKCOMMAND$&h=$HOSTNAME$&d=$HOSTPERFDATA$" \
             "http://localhost:8099/perfdata/store"
    }


    # 'process-service-perfdata' command definition
    define command{
            command_name    process-service-perfdata
            command_line    curl -d "l=$LASTSERVICECHECK$&c=$SERVICECHECKCOMMAND$&h=$HOSTNAME$&s=SERVICEDESC&d=$SERVICEPERFDATA$" \
            "http://localhost:8099/perfdata/store"
    }
