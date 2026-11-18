-- SQLite-compatible schema
CREATE TABLE customers (
  CustomerID TEXT PRIMARY KEY,
  County TEXT,
  CustomerType TEXT
);
CREATE TABLE transactions (
  TransactionID TEXT PRIMARY KEY,
  CustomerID TEXT NOT NULL,
  TransactionDate DATE NOT NULL,
  AmountKES DECIMAL(12,2) NOT NULL,
  Channel TEXT,
  FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID)
);
