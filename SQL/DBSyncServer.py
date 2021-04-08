# DB Sync Server
# Receive records.db from one client at a time. Show error in client if another tries to connect.
# From the client database, get items with isSynced == FALSE, and replace in local (master) DB
# Set isSynced = TRUE for all items in server DB and send to client.

