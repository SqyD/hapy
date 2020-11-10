# These are the Cards class definition for the upyhome package.

class HACard:
    def __init__(self, card_id, card_config):
        self.card_id = card_id
        self.type = card_config['type']
        self.config = card_config
        self.entities = []
        self.states = {}
        if 'icon' in card_config:
            self.icon = card_config['icon']

    def get_name(entity_id):
        if self.entities[entity_id]['attributes']['friendly_name']:
            name = self.entities[entity_id]['attributes']['friendly_name']
        else:
            name = entity_id.split(".")[1]
            words = name.split("_")
            for i in range(len(words)):
                words[i] = words[i][:1].upper() + words[i][1:].lower()
            name = " ".join(words)
        return name

    def get_icon(self, entity_id):
        if 'icon' in self.states[entity_id]['attributes']:
            icon = self.entities[entity_id]['attributes']['icon']
        else:
            domain = entity_id.split(".")[0]
            if 'device_class' in self.states[entity_id]['attributes']:
                device_class = self.entities[entity_id]['attributes']['device_class']
                icon = self.get_default_icon(domain, device_class)
            else:
                icon = self.get_default_icon(domain)
        return icon

    def get_default_icon(self, domain, device_class = None):
        if domain == 'light':
            return 'mdi:lightbulb'
        elif domain == 'fan':
            return 'mdi:fan'

    def set_elements(self):
        self.elements = {}


class HACardSingle(HACard):
    def __init__(self, card_id, card_config):
        super().__init__(card_id, card_config)
        self.entities.append(card_config['entity'])
        if 'name' in card_config:
            self.name = card_config['name']

class HACardEntity(HACardSingle):
    def set_elements(self):
        super().set_elements()
        self.elements['entity'] = {}
        if 'name' in self.config:
            self.elements['entity']['name'] = self.config['name']
        else:
            self.elements['entity']['name'] = self.get_name(self.entities[0])

        self.elements['entity']['icon'] = self.get_icon(self.entities[0])
        # self.elements.entity['state']


class HACardLight(HACardSingle):
    def __init__(self, card_id, card_config):
        super().__init__(card_id, card_config)

class HACardMulti(HACard):
    def __init__(self, card_id, card_config):
        super().__init__(card_id, card_config)
        if isinstance(card_config['entities'], list):
            self.entities = card_config['entities']
        elif isinstance(card_config['entities'], dict):
            self.entity_options = {}
            for entity in card_config['entities']:
                self.entities.append(entity['entity_id'])

    def set_elements(self):
        super().set_elements()

class HACardEntities(HACardMulti):
    def __init__(self, card_id, card_config):
        super().__init__(card_id, card_config)

# self.title = card_config['title']