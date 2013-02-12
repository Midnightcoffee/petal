from petalapp import db
from pci_notes.storage.market_organization import market_organization

def add_unique(name, table): #FIXME include question_option.. probable sql function
    n = table.query.filter_by(name=name).first()
    if not n:
        n = table(name=name)
        db.session.add(n)
        db.session.commit()
    return n

def number_organizations(market_organization):
    number = 0
    for k in market_organization:
        number += len(market_organization[k])
    return number

number_of_organizations = number_organizations(market_organization)

