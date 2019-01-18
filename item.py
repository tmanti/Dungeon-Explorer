import xml.etree.ElementTree as ET
import spritesheet
import dataTypes

#SlotTypes
# 1-warrior 2 special 3 heavy armour
# 4-mage    5 special 6 robes
# 7-ranger  8 special 9 hides
# 10 - rings
#11 - usbale by all


class spriteRef:
    def __init__(self, spriteFile, index, foldername):
        self.fileLocation = "resources/Sprites/" + foldername + "/" + spriteFile.lower() + ".png"
        self.index = index.split("x")
        for x in range(len(self.index)):
            #print(x)
            self.index[x] = int(self.index[x])*8

    def __str__(self):
        return "[%s, %s]" % (self.index, self.fileLocation)

class Material:
    def __init__(self, name, type, itemClass, slotType, desc, tier=None, texture=None, rateOfFire = None, damage = None, range=None, projectile=None, use=[]):
        self.name = name
        self.type = type
        self.itemClass = itemClass
        if texture:
            self.Texture = texture
            ss = spritesheet.spritesheet(self.Texture.fileLocation)
            self.image = ss.image_at((self.Texture.index[0], self.Texture.index[1], 8, 8), colorkey=dataTypes.WHITE)
        else:
            self.Texture = None
        if projectile:
            self.projectile = projectile
        self.SlotType = slotType
        self.description = desc
        self.tier = tier
        self.rateOfFire = rateOfFire
        self.damage = damage
        self.range = range
        self.useMeta = use

        self.__repr__ = self.__str__


    def use(self):
        if self.itemClass == "equipment":
            pass

    def __str__(self):
        return "<%s type=%s id=%s {SlotType=%s, description=%s, Texture=%s}>" % (self.itemClass, self.type, self.name, self.SlotType, self.description, self.Texture)

class ItemStack:
    def __init__(self, amount, material):
        self.amount = amount
        self.material = material

    def return_Itemstack(self):
        return [self.amount, self.material]

Nothing = Material("None", "0xfff", "None", None, None, None)
allItems = {"0xfff":Nothing}
Equipment = {}

#https://docs.python.org/3/library/xml.etree.elementtree.html
def init():
    tree = ET.parse("resources/xml/items.xml")
    root = tree.getroot()
    for child in root:
        #print(child.tag, child.attrib)
        itemClass = child.find('Class').text

        if itemClass == "Equipment" and child.find("Weapon")!= None:
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
            Equipment[child.get('type')] = allItems[child.get('type')]
        elif itemClass == "Consumable" and child.find("Item") != None:
            allItems[child.get('type')] = Material(child.get('id'),
                                                   child.get('type'),
                                                   itemClass,
                                                   child.find("SlotType"),
                                                   child.find("Description"),
                                                   texture=spriteRef(child.find("Texture").find("File").text, child.find("Texture").find("Index").text, "items"),
                                                   use=[child.find("Use").find("Action"), child.find("Use").find("Amount")])