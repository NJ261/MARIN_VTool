| Path | Description |
| ---- | ----------- |
| Config/ | Sample xml files for db connection and SSH tunnel |
| Tests/ | Unit tests |

### SSHTunnel
Start a new process which create a ssh tunnel.
```python
import SSHTunnel

# read config xml file, refer to sample file: Config/SampleSSHConfig.xml
sshTunnel = SSHTunnel.SSHTunnel('Config/SampleSSHConfig.xml')

# start new process: create ssh tunnel
sshSubprocess = sshTunnel.startTunnel()

# stop process: kill connection
sshTunnel.stopTunnel(sshSubprocess)
```

### DB Connection
Create a DB connection.
```python
import DBConnection

# read config xml file, refer to the sample file: Config/SampleDBConfig.xml
dbConnection = DBConnection.DBConnection('Config/SampleDBConfig.xml')

# get connection
connection = dbConnection.getConnection()

# sample usage, refer to psycopg2 documentation: http://initd.org/psycopg/docs/
cursor = connection.cursor()
cursor.execute("SELECT * FROM table_A;")

# close connection
dbConnection.closeConnection(cursor, connection)
```