from PIL import Image, ImageTk
from countries import Country
from territory import Territory
from army import Army
import random
import json
import os
import tkinter as tk
class MainGame:
    def __init__(self):
        self.countries = {}
        self.territories = {}
        self.current_turn = 0
        self.max_turns = 20
        self.player_country = None
        self.territory_connections = {
            "柏林": ["慕尼黑", "维也纳", "华沙", "汉堡"],
            "汉堡": ["柏林", "伦敦"],
            "慕尼黑": ["柏林", "维也纳", "威尼斯"],
            "维也纳": ["慕尼黑", "威尼斯"],
            "华沙": ["柏林", "莫斯科"],
            "莫斯科": ["华沙"],
            "罗马": ["威尼斯", "巴黎"],
            "威尼斯": ["罗马", "巴黎"],
            "巴黎": ["罗马", "威尼斯", "伦敦"],
            "伦敦": ["巴黎", "汉堡"]
        }
    
    def initialize_game(self):
        # 创建国家
        self.countries = {
            "德国": Country("德国"),
            "英国": Country("英国"),
            "法国": Country("法国"),
            "苏联": Country("苏联"),
            "意大利": Country("意大利"),
            "波兰": Country("波兰"),
            "芬兰": Country("芬兰"),
            "挪威": Country("挪威"),
            "奥地利": Country("奥地利"),
            "瑞典": Country("瑞典"),
            "匈牙利": Country("匈牙利"),
            "罗马尼亚": Country("罗马尼亚"),
            "保加利亚": Country("保加利亚"),
            "南斯拉夫": Country("南斯拉夫"),
            "希腊": Country("希腊"),
            "捷克斯洛伐克": Country("捷克斯洛伐克")
        }
        
        self.player_country = "德国"
        self.countries[self.player_country].is_player = True
        
        # 创建领土
        european_territories = [
            # 德国
            ("柏林", 80, 25), ("慕尼黑", 60, 18), ("汉堡", 70, 20), 
            ("科隆", 55, 16), ("法兰克福", 65, 19), ("斯图加特", 50, 15),
            ("纽伦堡", 45, 14), ("莱比锡", 50, 15), ("多特蒙德", 55, 16),
            # 英国
            ("伦敦", 75, 22), ("利物浦", 60, 18), ("曼彻斯特", 55, 17),
            ("伯明翰", 50, 15), ("格拉斯哥", 45, 14), ("爱丁堡", 40, 12),
            ("贝尔法斯特", 35, 11), ("纽卡斯尔", 40, 12), ("朴茨茅斯", 45, 14),
            # 法国
            ("巴黎", 70, 21), ("马赛", 55, 17), ("里昂", 60, 18),
            ("图卢兹", 45, 14), ("尼斯", 40, 12), ("波尔多", 50, 15),
            ("里尔", 45, 14), ("斯特拉斯堡", 50, 15), ("南特", 40, 12),
            # 苏联
            ("莫斯科", 90, 30), ("列宁格勒", 70, 22), ("斯大林格勒", 65, 20),
            ("基辅", 60, 19), ("明斯克", 55, 17), ("哈尔科夫", 50, 16),
            ("敖德萨", 45, 15), ("斯摩棱斯克", 40, 13), ("塔林", 35, 11),
            # 意大利
            ("罗马", 60, 19), ("米兰", 65, 20), ("威尼斯", 55, 17),
            ("那不勒斯", 50, 16), ("都灵", 45, 14), ("佛罗伦萨", 40, 13),
            ("热那亚", 45, 14), ("博洛尼亚", 40, 12), ("巴勒莫", 35, 11),
            ("华沙", 55, 17), ("克拉科夫", 45, 14), ("格但斯克", 40, 13),  # 波兰
            ("维也纳", 60, 18), ("格拉茨", 40, 12), ("因斯布鲁克", 35, 11),  # 奥地利
            ("赫尔辛基", 50, 16), ("图尔库", 35, 11), ("坦佩雷", 30, 10),  # 芬兰
            ("奥斯陆", 45, 14), ("卑尔根", 35, 11), ("特隆赫姆", 30, 10),  # 挪威
            ("斯德哥尔摩", 55, 17), ("哥德堡", 45, 14), ("马尔默", 40, 13),  # 瑞典
            ("布达佩斯", 50, 16), ("德布勒森", 35, 11), ("塞格德", 30, 10),  # 匈牙利
            ("布加勒斯特", 45, 14), ("康斯坦察", 35, 11), ("雅西", 30, 10),  # 罗马尼亚
            ("索菲亚", 40, 13), ("普罗夫迪夫", 30, 10), ("瓦尔纳", 25, 9),  # 保加利亚
            ("贝尔格莱德", 45, 14), ("萨格勒布", 35, 11), ("萨拉热窝", 30, 10),  # 南斯拉夫
            ("雅典", 40, 13), ("塞萨洛尼基", 30, 10), ("帕特雷", 25, 9),  # 希腊
            ("布拉格", 50, 16), ("布尔诺", 35, 11), ("俄斯特拉发", 30, 10)  # 捷克斯洛伐克
        ]
        
        # 设置领土连接
        self.territory_connections = {
            "柏林": ["华沙", "汉堡", "莱比锡", "布拉格"],
            "慕尼黑": ["维也纳", "纽伦堡", "斯图加特", "因斯布鲁克"],
            "汉堡": ["柏林", "科隆", "不莱梅", "基尔"],
            "法兰克福": ["科隆", "斯图加特", "纽伦堡", "莱比锡"],
            "伦敦": ["利物浦", "伯明翰", "朴茨茅斯", "多佛尔"],
            "利物浦": ["曼彻斯特", "格拉斯哥", "都柏林"],
            "朴茨茅斯": ["南安普顿", "普利茅斯", "加来"],
            "巴黎": ["里尔", "斯特拉斯堡", "里昂", "南特"],
            "马赛": ["里昂", "尼斯", "图卢兹", "热那亚"],
            "斯特拉斯堡": ["法兰克福", "斯图加特", "苏黎世"],
            "莫斯科": ["列宁格勒", "斯摩棱斯克", "哈尔科夫", "明斯克"],
            "斯大林格勒": ["罗斯托夫", "哈尔科夫", "萨拉托夫"],
            "基辅": ["明斯克", "敖德萨", "哈尔科夫", "利沃夫"],
            "罗马": ["佛罗伦萨", "那不勒斯", "威尼斯"],
            "米兰": ["都灵", "热那亚", "威尼斯", "苏黎世"],
            "威尼斯": ["维也纳", "的里雅斯特", "博洛尼亚"],
            "维也纳": ["布拉格", "布达佩斯", "格拉茨", "威尼斯"],
            "华沙": ["柏林", "布拉格", "维尔纽斯", "利沃夫"],
            "赫尔辛基": ["塔林", "斯德哥尔摩", "列宁格勒"],
            "奥斯陆": ["哥德堡", "斯德哥尔摩", "卑尔根"],
            "布达佩斯": ["维也纳", "布拉格", "贝尔格莱德", "布加勒斯特"]
        }
        
        # 设置初始控制领土
        self.countries["德国"].controlled_territories = ["柏林", "汉堡", "慕尼黑", "科隆", "法兰克福"]
        self.countries["英国"].controlled_territories = ["伦敦", "利物浦", "曼彻斯特", "伯明翰"]
        self.countries["法国"].controlled_territories = ["巴黎", "马赛", "里昂", "斯特拉斯堡"]
        self.countries["苏联"].controlled_territories = ["莫斯科", "列宁格勒", "斯大林格勒", "基辅"]
        self.countries["意大利"].controlled_territories = ["罗马", "米兰", "威尼斯", "那不勒斯"]
        self.countries["波兰"].controlled_territories = ["华沙", "克拉科夫", "格但斯克"]
        self.countries["奥地利"].controlled_territories = ["维也纳", "格拉茨"]
        self.countries["芬兰"].controlled_territories = ["赫尔辛基"]
        self.countries["挪威"].controlled_territories = ["奥斯陆"]
        self.countries["瑞典"].controlled_territories = ["斯德哥尔摩"]
        self.countries["匈牙利"].controlled_territories = ["布达佩斯"]
        self.countries["罗马尼亚"].controlled_territories = ["布加勒斯特"]
        self.countries["保加利亚"].controlled_territories = ["索菲亚"]
        self.countries["南斯拉夫"].controlled_territories = ["贝尔格莱德"]
        self.countries["希腊"].controlled_territories = ["雅典"]
        self.countries["捷克斯洛伐克"].controlled_territories = ["布拉格"]
        
        # 创建领土对象
        for name, res, strat in european_territories:
            self.territories[name] = Territory(name, res, strat)
        
        # 初始军队
        initial_armies = {
            "德国": 15, "苏联": 12, "英国": 10, "法国": 10, 
            "意大利": 8, "波兰": 6, "瑞典": 5, "匈牙利": 4,
            "罗马尼亚": 4, "奥地利": 5, "芬兰": 3, "挪威": 3,
            "保加利亚": 3, "南斯拉夫": 4, "希腊": 3, "捷克斯洛伐克": 5
        }
        
        for country_name, country in self.countries.items():
            army_size = initial_armies.get(country_name, 3)
            for territory in country.controlled_territories:
                required = army_size * 10
                if country.resources < required:
                    country.resources = required
                if country.manpower < army_size:
                    country.manpower = army_size
                if country.recruit_army(army_size):
                    self.territories[territory].add_army(country.armies[-1])
                    self.territories[territory].controlling_country = country.name
                else:
                    print(f"错误: {country_name} 无法在 {territory} 部署军队，使用后备方案")
                    country.resources = max(country.resources, 100)
                    country.manpower = max(country.manpower, 100)
                    country.recruit_army(3)
                    self.territories[territory].add_army(country.armies[-1])
                    self.territories[territory].controlling_country = country.name
    
    def move_army(self, from_territory_name, to_territory_name, army_index):
        if from_territory_name not in self.territories or to_territory_name not in self.territories:
            return "错误：领土不存在"
        from_territory = self.territories[from_territory_name]
        to_territory = self.territories[to_territory_name]
        if from_territory.controlling_country != self.player_country:
            return "错误：你只能移动自己领土的军队"
        if to_territory_name not in self.territory_connections.get(from_territory_name, []):
            return "错误：只能移动到相邻领土"
        if army_index < 0 or army_index >= len(from_territory.armies):
            return "错误：无效的军队索引"
        army = from_territory.armies[army_index]
        if to_territory.controlling_country == self.player_country:
            from_territory.remove_army(army)
            to_territory.add_army(army)
            return f"成功将军队从 {from_territory_name} 移动到 {to_territory_name}"
        else:
            return self.attack_territory(from_territory_name, to_territory_name, army_index)
    
    def attack_territory(self, from_territory_name, to_territory_name, army_index):
        from_territory = self.territories[from_territory_name]
        to_territory = self.territories[to_territory_name]
        attacking_army = from_territory.armies[army_index]
        if not to_territory.armies:
            from_territory.remove_army(attacking_army)
            to_territory.add_army(attacking_army)
            to_territory.controlling_country = self.player_country
            self.countries[self.player_country].controlled_territories.append(to_territory_name)
            old_owner = to_territory.controlling_country
            if old_owner:
                self.countries[old_owner].controlled_territories.remove(to_territory_name)
            return f"成功占领 {to_territory_name}!"
        defending_army = to_territory.armies[0]
        attack_power = attacking_army.size * (1 + attacking_army.experience * 0.1) * random.uniform(0.8, 1.2)
        defense_power = defending_army.size * (1 + defending_army.experience * 0.1) * random.uniform(0.8, 1.2)
        if attack_power > defense_power:
            from_territory.remove_army(attacking_army)
            to_territory.add_army(attacking_army)
            old_owner = to_territory.controlling_country
            to_territory.controlling_country = self.player_country
            self.countries[self.player_country].controlled_territories.append(to_territory_name)
            if old_owner:
                self.countries[old_owner].controlled_territories.remove(to_territory_name)  
            defending_army.size = max(1, int(defending_army.size * 0.5))
            return (f"战斗胜利！占领 {to_territory_name}\n"
                    f"你的军队剩余: {attacking_army.size}\n"
                    f"敌方军队剩余: {defending_army.size}")
        else:
            attacking_army.size = max(1, int(attacking_army.size * 0.6))
            defending_army.size = max(1, int(defending_army.size * 0.8))
            return (f"战斗失败！\n"
                    f"你的军队剩余: {attacking_army.size}\n"
                    f"敌方军队剩余: {defending_army.size}")
    
    def ai_turn(self):
        for country_name, country in self.countries.items():
            if country_name != self.player_country and country.armies:
                for army in country.armies:
                    if army.location and random.random() > 0.5:
                        possible_targets = [t for t in self.territories.values()
                                        if t != army.location and t.controlling_country != country_name]
                        if possible_targets:
                            target = random.choice(possible_targets)
                            if target.controlling_country:
                                defending_army = random.choice(target.armies)
                                attack_power = army.size * (1 + army.experience * 0.1) * random.uniform(0.8, 1.2)
                                defense_power = defending_army.size * (1 + defending_army.experience * 0.1) * random.uniform(0.8, 1.2)
                                if attack_power > defense_power:
                                    old_controller = self.countries[target.controlling_country]
                                    old_controller.controlled_territories.remove(target.name)
                                    country.controlled_territories.append(target.name)
                                    target.controlling_country = country.name
                                    defending_army.size = max(1, defending_army.size // 2)
                            else:
                                army.location.remove_army(army)
                                target.add_army(army)
    
    def resolve_battle(self, attacking_army, defending_army):
        attack_power = attacking_army.size * (1 + attacking_army.experience * 0.1)
        defense_power = defending_army.size * (1 + defending_army.experience * 0.1)
        attack_power *= random.uniform(0.8, 1.2)
        defense_power *= random.uniform(0.8, 1.2)
        return attack_power > defense_power
    
    def next_turn(self):
        self.current_turn += 1
        for country in self.countries.values():
            country.produce_resources()
            if random.random() > 0.7:
                country.recruit_army(random.randint(5, 15))
        self.ai_turn()
    
    def check_victory(self):
        territory_count = {name: 0 for name in self.countries}
        for territory in self.territories.values():
            if territory.controlling_country:
                territory_count[territory.controlling_country] += 1
        total_territories = len(self.territories)
        for country, count in territory_count.items():
            if count >= (total_territories // 2) + (1 if total_territories % 2 != 0 else 0):
                return country
        return None
    
    def save_game(self, filename):
        game_state = {
            "countries": {name: {
                "resources": c.resources,
                "manpower": c.manpower,
                "controlled_territories": c.controlled_territories,
                "is_player": c.is_player
            } for name, c in self.countries.items()},
            "territories": {name: {
                "controlling_country": t.controlling_country,
                "armies": [{
                    "size": a.size,
                    "country": a.country,
                    "experience": a.experience
                } for a in t.armies]
            } for name, t in self.territories.items()},
            "current_turn": self.current_turn,
            "player_country": self.player_country
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)
    
    def load_game(self, filename):
        with open(filename, 'r') as f:
            game_state = json.load(f)
        self.countries = {}
        for name, data in game_state["countries"].items():
            country = Country(name, data["is_player"])
            country.resources = data["resources"]
            country.manpower = data["manpower"]
            country.controlled_territories = data["controlled_territories"]
            self.countries[name] = country
        self.territories = {}
        for name, data in game_state["territories"].items():
            territory = Territory(name, 0, 0)
            territory.controlling_country = data["controlling_country"]
            for army_data in data["armies"]:
                army = Army(army_data["size"], army_data["country"])
                army.experience = army_data["experience"]
                territory.add_army(army)
                self.countries[army.country].armies.append(army)
            self.territories[name] = territory
        self.current_turn = game_state["current_turn"]
        self.player_country = game_state["player_country"]
    
    def show_map_window(self):
        goal = ["europe_map.jpg", "europe_map.png", "map.jpg", "map.png", "ww2_map.jpg"]
        img_file = None
        for file in goal:
            if os.path.exists(file):
                img_file = file
                break
        if img_file is None:
            print("[error]:找不到地图图片文件")
            print("请将地图图片放在游戏目录下,支持的文件名:")
            for file in goal:
                print(f" - {file}")
            input("按回车键继续...")
            return
        try:
            window = tk.Tk()
            window.title("map")
            img = Image.open(img_file)
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            img_width, img_height = img.size
            if img_width > screen_width * 0.8 or img_height > screen_height * 0.8:
                img = img.resize((int(screen_width * 0.8), int(screen_height * 0.8)))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(window, image=photo)
            label.pack()
            window.mainloop()
        except Exception as e:
            print(f"打开地图时出错: {e}")
            print("若多次尝试依然报错,请手动打开地图图片文件")
            input("按回车键继续...")