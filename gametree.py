

class GameInfo:
    def __init__(self, punktu_skaits:int,sak_dators:bool,izmantot_alfa_beta:bool):
        self.punktu_skaits=punktu_skaits
        self.speles_garums=punktu_skaits/2
        self.sak_dators=sak_dators
        self.izmantot_alfa_beta=izmantot_alfa_beta
        return

class GameState:
    def __init__(self, linijas: list[tuple[int,int]]=[], p1_punkti : int=0, p2_punkti : int=0):
        self.linijas = linijas
        self.p1_punkti = p1_punkti
        self.p2_punkti = p2_punkti
        return



class Node:
    def __init__(self, gamestate:GameState, level,gameinfo:GameInfo):
        self.gamestate=gamestate
        self.level=level
        self.gameinfo=gameinfo

    def children(self):
        esosas_linijas=self.gamestate.linijas
        if (not esosas_linijas):
            izmantotie_punkti=set()
        else:
            izmantotie_punkti=set([item for sublist in esosas_linijas for item in sublist])
        visi_punkti=set(list(range(self.gameinfo.punktu_skaits)))
        brivie_punkti=visi_punkti-izmantotie_punkti

        jaunais_limenis=self.level+1
        new_nodes=[]
        for start_point in brivie_punkti:
            for end_point in brivie_punkti:
                if end_point<=start_point:
                    continue
                jauna_linija=(start_point,end_point)
                jaunas_linijas=esosas_linijas.copy()
                jaunas_linijas.append(jauna_linija)
                p1_new=self.gamestate.p1_punkti
                p2_new=self.gamestate.p2_punkti
                sods=points_when_add_line(esosas_linijas,jauna_linija)
                if jaunais_limenis%2==1:
                    p1_new+=sods
                else:
                    p2_new+=sods
                new_nodes.append(Node(GameState(jaunas_linijas,p1_new,p2_new),jaunais_limenis,self.gameinfo))
        return new_nodes
                
    def score(self):
        return self.gamestate.p2_punkti-self.gamestate.p1_punkti

def NextMove(current_node:Node,gameinfo:GameInfo,max_depth)->Node:
    children=current_node.children()
    best_child=None
    if(not gameinfo.izmantot_alfa_beta):
        if gameinfo.sak_dators :
            value=-1e16
            for child in children:
                child_score=MinMax(child, max_depth, False)
                if child_score>value:
                    best_child=child
                    value=child_score
            return best_child
        else:
            value = 1e16
            for child in children:
                child_score=MinMax(child, max_depth, False)
                if child_score<value:
                    best_child=child
                    value=child_score
    elif(gameinfo.izmantot_alfa_beta):
        if gameinfo.sak_dators :
            value=-1e16
            for child in children:
                child_score=AlphaBeta(child, max_depth, False)
                if child_score>value:
                    best_child=child
                    value=child_score
            return best_child
        else:
            value = 1e16
            for child in children:
                child_score=AlphaBeta(child, max_depth, False)
                if child_score<value:
                    best_child=child
                    value=child_score
    
            return best_child

def MinMax(start_node:Node,depth:int,is_p1): #p1 is always maximizing, easier to remember this way though
    print(depth)

    children=start_node.children()
    if depth == 0 or not children:
        return start_node.score()
    if is_p1 :
        value=-1e16
        for child in children:
            value = max(value, MinMax(child, depth-1, False))
        return value
    else:
        value = 1e16
        for child in children:
            value = min(value, MinMax(child, depth-1, True))
        return value

def AlphaBeta(start_node:Node,depth:int,is_p1,alpha=-1e16,beta=1e16): #p1 is always maximizing, easier to remember this way though
    print(depth)
    children=start_node.children()
    if depth == 0 or not children:
        return start_node.score()
    if is_p1 :
        value=-1e16
        for child in children:
            value = max(value, AlphaBeta(child, depth-1, False,alpha,beta))
            if value > beta:
                break
            alpha=max(alpha,value)
        return value
    else:
        value = 1e16
        for child in children:
            value = min(value, AlphaBeta(child, depth-1, True,alpha,beta))
            if value < alpha:
                break
            beta=min(beta,value)
        return value                  

def points_when_add_line(linijas, jauna_linija):
    sods=0
    for line in linijas:
        sods+=int(does_line_cross(jauna_linija,line))
    return sods


def does_line_cross(linija_jauna:tuple[int,int],linija_veca:tuple[int,int]):
    sakums_vecai=min(linija_veca)
    beigas_vecai=max(linija_veca)
    #tagad parbaudam vai abi jaunas linija punkti ir viena puse vecajai
    sakums_starp=linija_jauna[0]>sakums_vecai and linija_jauna[0]<beigas_vecai
    beigas_starp=linija_jauna[1]>sakums_vecai and linija_jauna[1]<beigas_vecai
    if(sakums_starp==beigas_starp):
        return False
    else:
        return True