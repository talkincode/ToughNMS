import os,sqlite3

def  create_sql(infile,outfile):

    print infile,outfile

    outfs = open(outfile,'wb')

    with open(infile,'rb') as infs:

        _start_table = False

        _end_table = False

        _current_table_args = None

        while 1:
            line = infs.next().strip()
            if not line:
                continue

            if '.. start_table' in line:
                _start_table = True
                _end_table = False
                _current_table_args = line[15:].strip().split(";")

                _commont_buf = "-- create table %s\r\n"%_current_table_args[0]
                outfs.write(_commont_buf)

                _table_begin_buf = "create table %s (\r\n"%_current_table_args[0]
                outfs.write(_table_begin_buf)

                line = infs.next()
                line = infs.next()  
                line = infs.next()                    
                continue

            if _start_table:
                
                cols = []
                print "start table process %s"%_current_table_args[0]
                while 1:
                    _line = infs.next()
                    if '.. end_table' in _line:
                        _end_table = True
                        _start_table = False

                        _cols_buf = ",\r\n".join(cols)
                        outfs.write(_cols_buf)
                        outfs.write(',\r\n')
                        outfs.write('\tprimary key ( %s )'%_current_table_args[1])
                        outfs.write('\r\n);\r\n')
               
                        print "end table process %s"%_current_table_args[0]
                        break
                    else:
                    
                        if  "==" in _line:
                            continue
                        else:
                            _cls = _line.split()
                            if _cls:
                                _bf = "    %s %s %s"%(_cls[0],_cls[1],(_cls[1]=='yes' and "null" or "not null"))
                                cols.append(_bf)

    print "done"

def build_db(doc_src,sql_file,db_file,model_file):
    try:
        create_sql(doc_src,sql_file)
    except StopIteration:
        pass
    try:
        os.unlink(db_file)
        os.unlink(model_file)
    except:
        pass
    con = sqlite3.connect(db_file)
    con.executescript(open(sql_file).read())
    os.popen("/usr/local/bin/sqlautocode sqlite:///%s -d -o %s"%(db_file,model_file))   

if __name__ == "__main__":
    build_db("database.rst","database.sql","database.sqlite3","db_models.py")

