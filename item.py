import xml.etree.ElementTree as ET
import spritesheet
import dataTypes

#SlotTypes
# 1-warrior 2 special 3 heavy armour
# 4-mage    5 special 6 robes
# 7-ranger  8 special 9 hides
# 10 - rings
#11 - usbale by all


class spriteRef:#sprite ref object
    def __init__(self, spriteFile, index, foldername):
        #store data
        self.fileLocation = "resources/Sprites/" + foldername + "/" + spriteFile.lower() + ".png"
        self.index = index.split("x")
        for x in range(2):#get location of sprite in terms of size
            #print(x)
            self.index[x] = int(self.index[x])*8

        if len(self.index) == 3:#multiply size if larger
            self.size = 8*int(self.index[2])
        else:
            self.size = 8

    def __str__(self):
        return "[%s, %s]" % (self.index, self.fileLocation)

class Material:#material object
    def __init__(self, name, type, itemClass, slotType, desc, tier=None, texture=None, rateOfFire = None, damage = None, range=None, projectile=None, use=[], group=None):
        #store all variables for easy use
        self.name = name
        self.type = type
        self.itemClass = itemClass
        if texture:
            self.Texture = texture
            ss = spritesheet.spritesheet(self.Texture.fileLocation)
            self.image = ss.image_at((self.Texture.index[0], self.Texture.index[1], self.Texture.size, self.Texture.size), colorkey=dataTypes.WHITE)
        else:
            self.Texture = None
            self.image = None
        if projectile:
            self.projectile = projectile
            ss = spritesheet.spritesheet(self.projectile.fileLocation)
            self.projectileImage = ss.image_at((self.projectile.index[0], self.projectile.index[1], self.Texture.size, self.Texture.size), colorkey=dataTypes.WHITE)
        self.SlotType = slotType
        self.description = desc
        self.tier = tier
        self.rateOfFire = rateOfFire
        self.damage = damage
        self.range = range
        self.useMeta = use
        self.group = group

        self.__repr__ = self.__str__

    def __str__(self):
        return "<%s type=%s id=%s {SlotType=%s, description=%s, Texture=%s}>" % (self.itemClass, self.type, self.name, self.SlotType, self.description, self.Texture)

class ItemStack:#itemstack object
    def __init__(self, amount, material):
        #store the amount of objects and the material
        self.amount = amount
        self.material = material

    def return_Itemstack(self):#return an array which has the item stack data
        return [self.amount, self.material]

Nothing = Material("None", "0xfff", "None", 11, None, None)#blank item
allItems = {"0xfff":Nothing}#all items

#https://docs.python.org/3/library/xml.etree.elementtree.html
def init():
    tree = ET.parse("resources/xml/items.xml")#get ref to items xml file
    root = tree.getroot()#get root
    for child in root:#for obeject
        #print(child.tag, child.attrib)
        itemClass = child.find('Class').text#get itemcallss

        if itemClass == "Equipment" and child.find("Weapon")!= None:#create material object for weapon type
            allItems[child.get('type')] = Material(child.get('id'),
                                                   child.get('type'),
                                                   itemClass,
                                                   child.find("SlotType").text,
                                                   child.find("Description").text,
                                                   tier=child.find("Tier"),
                                                   texture=spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "items"),
                                                   rateOfFire=int(child.find("RateOfFire").text),
                                                   damage=[int(_) for _ in child.find("Damage").text.split("-")],
                                                   range=int(child.find("Range").text),
                                                   projectile=spriteRef(child.find("ProjectileTexture").find("File").text, child.find("ProjectileTexture").find("Index").text, "items"))
        elif itemClass == "Equipment" and child.find("Special")!= None:#create material for special type
            allItems[child.get('type')] = Material(child.get('id'),
                                                   child.get('type'),
                                                   itemClass,
                                                   child.find("SlotType").text,
                                                   child.find("Description").text,
                                                   tier="UT",
                                                   texture=spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "items"),
                                                   use=[child.find("Use").find("Action").text, child.find("Use").find("Amount").text])
        elif itemClass == "Consumable" and child.find("Item") != None:#create material for consumable type
            allItems[child.get('type')] = Material(child.get('id'),
                                                   child.get('type'),
                                                   itemClass,
                                                   child.find("SlotType").text,
                                                   child.find("Description").text,
                                                   group=child.find("Group").text,
                                                   texture=spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "items"),
                                                   use=[child.find("Use").find("Action").text, child.find("Use").find("Amount").text])