# Odoo Tutorial Estate App

Just the odoo tutorial from 
[odoo page](https://www.odoo.com/documentation/19.0/developer/tutorials/server_framework_101.html).

## Run the addon
```sh
./odoo-bin --addons-path='../estate_addons' -c odoo.conf -d rd-demo -u estate --dev xml
```

## Test

### Enabled test
```sh
./odoo-bin --addons-path='../estate_addons' -c odoo.conf -d rd-demo -i estate --test-enable
```

### Run test
```sh
./odoo-bin --addons-path='../estate_addons' -c odoo.conf -d rd-demo --test-file=../estate_addons/estate/tests/test_property.py
```

## Current State

Chapter 6
