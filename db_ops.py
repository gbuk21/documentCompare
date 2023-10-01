import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
def connect():
   conn = sqlite3.connect('doc_compare_db.db',check_same_thread=False)
   return conn

def close(conn):
   conn.close()



def get_doc_differences(conn, user_id, path, CurrentVersion, previousversion):
    conn.row_factory = dict_factory
    #print("select * from document_differences w ")
    cursor = conn.execute("select * from document_differences w where path  ='"+str(path)+"' and (CurrentVersion  ='"+str(CurrentVersion)+"' and previousversion  ='"+str(previousversion)+"') or previousversion  ='"+str(CurrentVersion)+"' and CurrentVersion  ='"+str(previousversion)+"'")    
    return(cursor.fetchall())
    
def get_distinct_documents(conn, user_id ):
    conn.row_factory = dict_factory
    #print("select word from words w  where not exists (select 1 from spelled_words  sw where sw.word_id = w.word_id and   user_id ="+str(user_id)+")  order by word_id")
    cursor = conn.execute("select distinct path from document_differences w   ")
    return(cursor.fetchall())

def get_distinct_document_versions(conn, user_id,path ):
    conn.row_factory = dict_factory
    cursor = conn.execute("select distinct CurrentVersion from document_differences w where path  ='"+str(path)+"' union select distinct  previousversion from document_differences w where path  ='"+str(path)+"'")
    return(cursor.fetchall())

def add_compare(conn, user_id , DatePerformed, Path, CurrentVersion, PreviousVersion, LineNumber, NewSentence, OldSentence):
    print("insert into document_differences( DatePerformed, Path, CurrentVersion, PreviousVersion, LineNumber, NewSentence, OldSentence ) values ('','document1','1.0','0.0', "+str(LineNumber)+" , '"+str(NewSentence)+"' , '"+str(OldSentence)+"') ")  
    cursor = conn.execute("insert into document_differences( DatePerformed, Path, CurrentVersion, PreviousVersion, LineNumber, NewSentence, OldSentence ) values ('','document1','1.0','0.0', "+str(LineNumber)+" , '"+str(NewSentence)+"' , '"+str(OldSentence)+"') ")        
    conn.commit() 





