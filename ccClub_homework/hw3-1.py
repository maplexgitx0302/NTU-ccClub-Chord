def find_helper(children):
    if len(children) > 4:
        mid = int(len(children)/2)
        if children[mid] < children[mid+1]:
            return find_helper(children[mid:]) + mid
        else:
            return find_helper(children[:mid+2])
    else:
        return children.index(max(children))