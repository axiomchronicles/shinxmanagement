from electrus.asynchronous import Electrus

client: Electrus = Electrus()
database = client["ShinxManagementDatabase"]

# ShinxManagement Collections :: pier 391

accountregistrationcollection = database["accountRegistrationCollection"]