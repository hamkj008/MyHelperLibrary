
# ========================================================================================

class ParentDelegatorMixin():
    """Provides automatic method delegation to a parent object.
    
    Classes using this mixin must set self._parent in their __init__.
    Once set, any method calls not found on the class will automatically
    delegate to the parent object. Used for INNER CLASSES
    """
    def __getattr__(self, name):
        return getattr(self._parent, name)

# ========================================================================================