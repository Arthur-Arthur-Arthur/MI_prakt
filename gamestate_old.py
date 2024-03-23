

class GameState:
    def __init__(self, linijas: list[tuple[int,int]]=[], p1_punkti : int=0, p2_punkti : int=0):
        self.linijas = linijas
        self.p1_punkti = p1_punkti
        self.p2_punkti = p2_punkti
        return


class Node:
    def __init__(self, gamestate:GameState, level,parent):
        self.gamestate=gamestate
        self.level=level
        self.parent=parent
        self.children=[]

class GameTree: 
    def __init__(self,punktu_skaits):
        self.punktu_skaits=punktu_skaits
        self.gajienu_skaits=punktu_skaits/2
        self.sakumvirsotne=Node(GameState(),0,None)
        self.limeni=[None]*(self.gajienu_skaits)
    def generate_new_nodes(self,node:Node):
        esosas_linijas=node.gamestate.linijas
        izmantotie_punkti=set([item for sublist in esosas_linijas for item in sublist])
        visi_punkti=set(list(range(self.punktu_skaits)))
        brivie_punkti=visi_punkti-izmantotie_punkti

        jaunais_limenis=node.level+1
        for start_point in brivie_punkti:
            for end_point in brivie_punkti:
                if end_point<=start_point:
                    break
                jauna_linija=(start_point,end_point)
                jaunas_linijas=esosas_linijas.copy().append(jauna_linija)
                p1_new=node.gamestate.p1_punkti
                p2_new=node.gamestate.p2_punkti
                sods=points_when_add_line(esosas_linijas,jauna_linija)
                if jaunais_limenis%2==0:
                    p1_new+=sods
                else:
                    p2_new+=sods
            
    def equals(state:GameState,other_state:GameState):
        return set(state.linijas)==set(other_state.linijas) and state.p1_punkti==other_state.p1_punkti and state.p2_punkti==other_state.p2_punkti

    def find_duplicate(self,node:Node):
        limenis=self.limeni[node.level]     
        for other_node in limenis:
            if node.gamestate.equals(other_node.gamestate):
                return other_node
        else: return node

                
                    

def points_when_add_line(linijas, jauna_linija):
    sods=0
    for line in linijas:
        sods+=int(does_line_cross(jauna_linija,line))
    return sods


def does_line_cross(linija_jauna:tuple[int,int],linija_veca:tuple[int,int]):
    sakums_vecai=min(linija_veca)
    beigas_vecai=max(linija_veca)
    #tagad parbaudam vai abi jaunas linija punkti ir viena puse vecajai
    sakums_starp=linija_jauna[0]>sakums_vecai and linija_jauna[0]>beigas_vecai
    beigas_starp=linija_jauna[1]>sakums_vecai and linija_jauna[1]>beigas_vecai
    if(sakums_starp==beigas_starp):
        return False
    else:
        return True