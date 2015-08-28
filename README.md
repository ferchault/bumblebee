# bumblebee
Interactive data store for analysing trajectory data using SQL/Tableau

Essentially, the idea is to transform trajectory or single point calculation data from arbitrary codes for atomistic simulations into a database. As relational databases have a hard time adding columns to existing database tables with several tens of millions of lines, a NoSQL interface is used. This gives the flexibility of a schemaless operation which allows quick annotations to the raw data. This way, all information (even intermediate one) can be stored in a single location which makes it easy to interface scripting and plotting. (Think: automatic updates of plots from simulations as the simulation goes on.)

This leverages the highly effective parallelisation and scaling mechanisms inherent to NoSQL data warehouses.
