import xml.etree.ElementTree as ET
import spritesheet
import dataTypes

#SlotTypes
# 1-warrior
# 2-mage
# 3-ranger
# 4 - useable by all


class spriteRef:
    def __init__(self, spriteFile, index):
        self.fileLocation = "resources/Sprites/" + spriteFile + "/" + spriteFile + ".png"
        self.index = index.split("x")
        for x in self.index:
            #print(x)
            x = int(x)*8

    def __str__(self):
        return "[%s, %s]" % (self.index, self.fileLocation)

class Material:
    def __init__(self, name, type, itemClass, isItem, file, index, slotType, desc, rateOfFire = None, damage = None, range=None, projectile=None):
        self.name = name
        self.type = type
        self.itemClass = itemClass
        self.isItem = isItem
        if file:
            self.Texture = spriteRef(file, index)
        else:
            self.Texture = None
        self.SlotType = slotType
        self.description = desc
        self.rateOfFire = rateOfFire
        self.damage = damage
        self.range = range

        self.__repr__ = self.__str__

        if self.Texture:
            ss = spritesheet.spritesheet(self.Texture.fileLocation)
            self.image = ss.image_at((self.Texture.index[0], self.Texture.index[1], 8, 8), colorkey=dataTypes.WHITE)

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

Nothing = Material("None", "0xfff", "None", None, None, None, 4, "", None)
allItems = {"0xfff":Nothing}
Weapons = {}

#https://docs.python.org/3/library/xml.etree.elementtree.html
def init():
    tree = ET.parse("resources/xml/items.xml")
    root = tree.getroot()
    for child in root:
        #print(child.tag, child.attrib)
        itemClass = child.find('Class').text
        if itemClass == "Equipment":
            allItems[child.get('type')] = Material(child.get('id'),
                                                   child.get('type'),
                                                   child.find("Class").text,
                                                   child.find("Item"),
                                                   child.find("Texture").find("File").text,
                                                   child.find("Texture").find("Index").text,
                                                   child.find("SlotType").text,
                                                   child.find("Description").text,
                                                   rateOfFire=int(child.find("RateOfFire").text),
                                                   damage=[int(_) for _ in child.find("Damage").text.split("-")],
                                                   range=int(child.find("Range").text))
        #print(child.get('id') + " : " + allItems[child.get('type')].Data())
