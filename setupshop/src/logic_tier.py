from cat_logic_tier import Domain_Logic as Cat_Domain_Logic
from cart_logic_tier import Domain_Logic as Cart_Domain_Logic
import ld4apps.aggregating_logic_tier as base 

class Domain_Logic(base.Domain_Logic):

    def create_logic_tier(self):
        all_parts = self.environ['PATH_INFO'].split('/')
        if not self.logic_tier:
            if all_parts[1] == 'cat': 
                self.logic_tier = Cat_Domain_Logic(self.environ)
            elif all_parts[1] == 'cart': 
                self.logic_tier = Cart_Domain_Logic(self.environ)
        return self.logic_tier
