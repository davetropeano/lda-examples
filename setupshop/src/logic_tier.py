from cat_logic_tier import Domain_Logic as Cat_Domain_Logic
from cart_logic_tier import Domain_Logic as Cart_Domain_Logic
import aggregating_logic_tier as base 

class Domain_Logic(base.Domain_Logic):

    def create_logic_tier(self):
        all_parts = self.environ['PATH_INFO'].split('/')
        if (self.logic_tier):
            raise ValueError('cannot use a domain_logic instance twice')
        else: 
            if all_parts[1] == 'cat': 
                self.logic_tier = Cat_Domain_Logic(self.environ)
            elif all_parts[1] == 'cart': 
                self.logic_tier = Cart_Domain_Logic(self.environ)
        return self.logic_tier
