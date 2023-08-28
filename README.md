# address_manager

A mailing address validator and manager.

Address Manager is a tool for cleaning and validating unstructured address data. Hand-entered addresses are imported
 in bulk, and then are compared against the Google and USPS databases to convert them to a deliverable format. Results can be exported to CSV for printing to address labels.

Address Manager has these features:

- Import your address data in any text format by pasting. No need to pre-separate the address components or meet a strict file upload specification.
- Manage validation, review, and confirmation all from the main page without reloading.
- Robust parsing and fuzzy-matching of unstructured data using Google's geocoding API
- Trustworthy verification that addresses are deliverable using USPS's address API
- Safe matching: if an address has a likely match which may not be correct, the user can review both addresses side-by-side and either confirm the match or edit the original input
- Discrete sets of addresses: The user can handle multiple different sets of addresses by specifying which to import to, and which to view on the overview page. (As of the 03-08-16 release, address sets must be created manually through the Django admin interface.)

Address Manager's source is hosted on [GitHub](https://github.com/alexthehurst/address_manager), and the app itself is hosted at <http://addressmanager.alexthehurst.com>.

The project makes use of [pyusps](https://github.com/thelinuxkid/pyusps) by Andres Buritica.
