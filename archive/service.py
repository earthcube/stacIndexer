# Add in provider as an Org or Person

def offer(url):
    o = {}

    o["@type"] = "Offer"
    o["itemOffered"] = service_instance(url)

    return o

def service_instance(url):
    s = {}
    pa = {}

    pa["@type"] = "Action"
    pa["target"] = url

    s["@type"] = "Service"
    s["description"] = "A STAC Catalog Service"

    s["potentialAction"] = pa

    return s

