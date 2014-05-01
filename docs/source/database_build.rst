数据库脚本工具
========================

数据字典描述
-----------------------

.. topic:: 注意

    在每个表格前增加一行注视，格式： .. 开始标记 表名;主键（注意联合主键的写法）

    表格前后保留一个空行

    在每个表格后增加一行注释，.. 结束标记
    
::

    .. start_table oms_stat_load;host_name,check_time

    =====================  ==============      ==========   =================
    属性                    类型（长度）         可否为空      字段描述
    =====================  ==============      ==========   =================
    host_name               varchar(64)         no           主机名
    avg_1                   varchar(8)          no           一分钟负载
    avg_5                   varchar(8)          no           五分钟负载
    avg_15                  varchar(8)          no           十五分钟负载
    check_time              varchar(19)         no           检测时间
    =====================  ==============      ==========   ==================

    .. end_table


数据库自动创建与sqlalchemy orm生成
-----------------------------------------

脚本由python编写,依赖模块sqlautocode,可使用pip安装::

    pip install sqlautocode

执行生成脚本::

    python builddb.py 

.. literalinclude:: builddb.py
   :language: python





