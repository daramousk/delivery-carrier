*Notes*

1) If this were to be submitted to the OCA, it should conform to the
guidelines (even if it were not submitted it would be a good practice to run
the pre-commit linters. (oca-gen-\*), black linting etc

2) Ftp connections can happen with public key cryptography, but this is out of
scope for now.

3) Run this by `docker compose up`, navigate to http://localhost:8069 and
follow the standard procedure to install the module. A new top menu will be
shown Import.

4) sftp functionality untested, not much time left

5) The csv files given are not well formed, what I would do is make sure that
what we get would be importable, there is no point in changing the data
received because its going to be very error prone and the code needed would
be double
