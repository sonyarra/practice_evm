import time
import os
import sys
import random

class FantasyDetective:
    def __init__(self):
        self.player_name = ""
        self.race = ""
        self.class_type = ""
        
        self.perception = 50      
        self.logic = 50           
        self.charisma = 50        
        self.magic = 0            
        

        self.inventory = {
            'увеличительное стекло': False,
            'дневник жертвы': False,
            'отравленный кинжал': False,
            'магический амулет': False,
            'странный порошок': False,
            'ключ от лаборатории': False,
            'заколка эльфийки': False,
            'кровь на платке': False
        }
        
        self.clues = []
        
        self.testimonies = {}
        
        self.suspects = {
            'Мираэль (эльфийка-артефактор)': {'виновна': False, 'допрошена': False, 'алиби': None},
            'Боргар (гном-алхимик)': {'виновна': False, 'допрошена': False, 'алиби': None},
            'Селен (человек-библиотекарь)': {'виновна': False, 'допрошена': False, 'алиби': None},
            'Верховный маг Аргус': {'виновна': False, 'допрошена': False, 'алиби': None}
        }
        
        self.murder_weapon = None
        self.motive = None
        self.real_killer = None
        self.crime_scene_investigated = False
        
        self.game_over = False
        self.murder_solved = False
        self.ending = None
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def slow_print(self, text, delay=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def print_separator(self):
        print("\n" + "="*60 + "\n")
    
    def print_header(self, text):
        print("\n" + "╔" + "═"*58 + "╗")
        print(f"║ {text:^56} ║")
        print("╚" + "═"*58 + "╝\n")
    
    def choice_maker(self, options):
        print("\nВаш выбор:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            try:
                choice = int(input("\n> "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(f"Введите число от 1 до {len(options)}")
            except ValueError:
                print("Пожалуйста, введите число")
    
    def update_stats(self, perception=0, logic=0, charisma=0):
        self.perception = max(0, min(100, self.perception + perception))
        self.logic = max(0, min(100, self.logic + logic))
        self.charisma = max(0, min(100, self.charisma + charisma))
        
        changes = []
        if perception != 0:
            changes.append(f"Внимательность: {'+' if perception>0 else ''}{perception}")
        if logic != 0:
            changes.append(f"Логика: {'+' if logic>0 else ''}{logic}")
        if charisma != 0:
            changes.append(f"Харизма: {'+' if charisma>0 else ''}{charisma}")
        
        if changes:
            print("\n[Навыки улучшены] " + ", ".join(changes))
    
    def show_stats(self):
        print("\n" + "─"*40)
        print(f"ХАРАКТЕРИСТИКИ {self.player_name}")
        print("─"*40)
        print(f"Раса: {self.race}")
        print(f"Класс: {self.class_type}")
        print(f"Внимательность: {self.perception}/100")
        print(f"Логика: {self.logic}/100")
        print(f"Харизма: {self.charisma}/100")
        if self.class_type == "Маг":
            print(f"Магическая сила: {self.magic}/100")
        print("─"*40)
    
    def show_inventory(self):
        print("\n" + "─"*40)
        print("ИНВЕНТАРЬ")
        print("─"*40)
        
        items_found = False
        for item, owned in self.inventory.items():
            if owned:
                print(f"✓ {item}")
                items_found = True
        
        if not items_found:
            print("Инвентарь пуст")
        
        if self.clues:
            print("\n НАЙДЕННЫЕ УЛИКИ:")
            for clue in self.clues:
                print(f"• {clue}")
        
        print("─"*40)
    
    def show_suspects_status(self):
        """Показать статус подозреваемых"""
        print("\n" + "─"*40)
        print(" ПОДОЗРЕВАЕМЫЕ")
        print("─"*40)
        
        for suspect, info in self.suspects.items():
            status = "🔍" if info['допрошена'] else "❌"
            alibi = f" - Алиби: {info['алиби']}" if info['алиби'] else ""
            print(f"{status} {suspect}{alibi}")
        
        print("─"*40)
    
    def create_character(self):
        self.clear_screen()
        self.print_header("СОЗДАНИЕ ПЕРСОНАЖА")
        
        self.slow_print("Вас зовут...")
        self.player_name = input("> ").strip()
        if not self.player_name:
            self.player_name = "Странник"
        
        self.slow_print(f"\nПриветствуем тебя, {self.player_name}!")
        time.sleep(1)
        
        self.print_separator()
        self.slow_print("Выберите свою расу:")
        race_options = ["Человек (универсальность, +5 ко всем навыкам)", 
                        "Эльф (+10 к внимательности, -5 к харизме среди гномов)", 
                        "Гном (+10 к логике, -5 к магии)"]
        
        race_choice = self.choice_maker(race_options)
        
        if race_choice == 1:
            self.race = "Человек"
            self.update_stats(perception=5, logic=5, charisma=5)
        elif race_choice == 2:
            self.race = "Эльф"
            self.update_stats(perception=10, logic=0, charisma=-5)
        else:
            self.race = "Гном"
            self.update_stats(perception=0, logic=10, charisma=0)
        
        self.slow_print(f"\nОтлично, {self.race} {self.player_name}!")
        self.slow_print("Теперь выберите свой класс:")
        class_options = ["Страж (сила и защита, +10 к логике в бою)", 
                         "Маг (магические способности, возможность использовать магию)", 
                         "Вор (скрытность и ловкость, +10 к внимательности)"]
        
        class_choice = self.choice_maker(class_options)
        
        if class_choice == 1:
            self.class_type = "Страж"
            self.update_stats(logic=10)
        elif class_choice == 2:
            self.class_type = "Маг"
            self.magic = 30
            self.slow_print("\nВы чувствуете поток магической энергии в жилах...")
        else:
            self.class_type = "Вор"
            self.update_stats(perception=10)
        
        self.slow_print(f"\nИтак, {self.race}-{self.class_type} {self.player_name} готов к приключениям!")
        time.sleep(2)
    
    def prologue(self):
        self.clear_screen()
        self.print_header("ПРОЛОГ: ТЕНЬ ЧЕРНОГО ЛЕСА")
        
        self.slow_print("Гильдия Магов города Эренделл потрясена ужасным событием...")
        time.sleep(1.5)
        self.slow_print("Верховный маг Аргус найден мертвым в своей лаборатории.")
        time.sleep(1.5)
        self.slow_print("Совет Гильдии в панике. Стража в замешательстве.")
        time.sleep(1.5)
        self.slow_print("И только ты, известный детектив, можешь раскрыть это преступление!")
        time.sleep(1.5)
        
        self.print_separator()
        self.slow_print("Прибыв в Гильдию Магов, ты видишь суету и перепуганных учеников.")
        self.slow_print("Магистр стражников встречает тебя у входа:")
        self.slow_print(f'"Детектив {self.player_name}! Слава богам, вы здесь! Это ужасно..."')
        
        input("\nНажмите Enter, чтобы продолжить...")
    
    def investigate_crime_scene(self):
        self.clear_screen()
        self.print_header("ОСМОТР МЕСТА ПРЕСТУПЛЕНИЯ")
        
        self.slow_print("Вы входите в лабораторию Верховного мага Аргуса.")
        self.slow_print("Помещение в беспорядке: книги разбросаны, зелья разлиты.")
        self.slow_print("Тело Аргуса лежит у алхимического стола.")
        
        self.print_separator()
        self.slow_print("Что вы хотите осмотреть в первую очередь?")
        
        investigation_options = [
            "Осмотреть тело жертвы",
            "Осмотреть алхимический стол",
            "Осмотреть книжные полки",
            "Поискать тайники (требует внимательность 60+)",
            "Закончить осмотр"
        ]
        
        investigating = True
        while investigating:
            choice = self.choice_maker(investigation_options)
            
            if choice == 1:  
                self.examine_body()
            elif choice == 2:  
                self.examine_table()
            elif choice == 3: 
                self.examine_bookshelf()
            elif choice == 4:  
                self.search_hiding_place()
            else:  
                investigating = False
            
            if investigating:
                input("\nНажмите Enter, чтобы продолжить осмотр...")
                self.clear_screen()
                self.print_header("ОСМОТР МЕСТА ПРЕСТУПЛЕНИЯ (продолжение)")
        
        self.crime_scene_investigated = True
        self.slow_print("\nВы закончили осмотр места преступления.")
    
    def examine_body(self):
        self.slow_print("\nВы подходите к телу Верховного мага Аргуса.")
        self.slow_print("На груди глубокая колотая рана. Смерть наступила несколько часов назад.")
        
        if self.perception >= 60:
            self.slow_print("Вы замечаете странные детали:")
            self.slow_print("1. Рана имеет неестественную форму - возможно, магическое оружие")
            self.slow_print("2. В руке жертвы зажат клочок пергамента")
            self.slow_print("3. Следы крови ведут к алхимическому столу, будто жертва пыталась ползти")
            
            self.clues.append("Неестественная рана (магическое оружие)")
            self.clues.append("Клочок пергамента в руке жертвы")
            self.update_stats(logic=5)
        else:
            self.slow_print("К сожалению, вашей внимательности недостаточно, чтобы заметить важные детали.")
            self.slow_print("Вы видите только то, что Аргус убит ударом в грудь.")
        
        self.slow_print("\nОбыскать тело?")
        search_choice = self.choice_maker(["Да", "Нет"])
        
        if search_choice == 1:
            self.slow_print("Вы обыскиваете карманы Аргуса...")
            if random.random() > 0.3:  # 70% шанс найти
                self.slow_print("Вы находите дневник жертвы!")
                self.inventory['дневник жертвы'] = True
                self.clues.append("Дневник с записями о конфликтах")
                self.update_stats(logic=5)
            else:
                self.slow_print("Ничего интересного не найдено.")
    
    def examine_table(self):
        self.slow_print("\nВы осматриваете алхимический стол.")
        self.slow_print("На столе стоят колбы с зельями, лежат ингредиенты.")
        
        if self.perception >= 50:
            self.slow_print("Вы замечаете странный порошок, рассыпанный на столе.")
            self.slow_print("Возможно, это яд?")
            
            take_poison = self.choice_maker(["Взять образец порошка", "Оставить как есть"])
            if take_poison == 1:
                self.inventory['странный порошок'] = True
                self.clues.append("Образец странного порошка")
                self.slow_print("Вы аккуратно собираете порошок в пузырек.")
        
        if self.perception >= 70:
            self.slow_print("\nПод столом вы замечаете отравленный кинжал!")
            self.slow_print("Клинок испачкан чем-то темным.")
            
            take_dagger = self.choice_maker(["Взять кинжал (улика)", "Не трогать (сохранить для экспертизы)"])
            if take_dagger == 1:
                self.inventory['отравленный кинжал'] = True
                self.clues.append("Отравленный кинжал (возможно орудие убийства)")
                self.update_stats(logic=5)
    
    def examine_bookshelf(self):
        self.slow_print("\nВы изучаете книжные полки.")
        self.slow_print("Множество древних фолиантов и свитков.")
        
        if self.logic >= 50:
            self.slow_print("Ваша логика подсказывает обратить внимание на книги по ядам.")
            self.slow_print("Одна из книг открыта на странице о редком эльфийском яде.")
            self.clues.append("Книга о ядах открыта на нужной странице")
            self.update_stats(logic=5)
        
        if self.perception >= 40:
            self.slow_print("\nМежду книг вы замечаете блестящий предмет.")
            self.slow_print("Это эльфийская заколка для волос!")
            
            take_hairpin = self.choice_maker(["Взять заколку (улика)", "Оставить"])
            if take_hairpin == 1:
                self.inventory['заколка эльфийки'] = True
                self.clues.append("Эльфийская заколка (не принадлежит жертве)")
    
    def search_hiding_place(self):
        if self.perception >= 60:
            self.slow_print("\nВы внимательно осматриваете комнату в поисках тайника.")
            self.slow_print("Ваша внимательность позволяет заметить неровность в каменной кладке.")
            self.slow_print("За камнем вы находите тайник!")
            
            #что в тайнике?
            secret_options = [
                "Открыть тайник (можно найти важные улики)",
                f"Попытаться взломать замок (шанс {(self.logic + self.perception)//2}%)"
            ]
            secret_choice = self.choice_maker(secret_options)
            
            if secret_choice == 1 or (secret_choice == 2 and random.randint(1, 100) < (self.logic + self.perception)//2):
                self.slow_print("Тайник открыт! Внутри вы находите:")
                self.slow_print("- Магический амулет с символом неизвестной организации")
                self.slow_print("- Письма, компрометирующие некоторых членов гильдии")
                self.slow_print("- Ключ от лаборатории")
                
                self.inventory['магический амулет'] = True
                self.inventory['ключ от лаборатории'] = True
                self.clues.append("Подозрительные письма")
                self.clues.append("Магический амулет тайной организации")
                self.update_stats(logic=10)
            else:
                self.slow_print("Замок слишком сложный. Вам не удается его открыть.")
        else:
            self.slow_print("\nВы ищете тайник, но вашей внимательности недостаточно.")
            self.slow_print("Возможно, стоит прокачать этот навык.")
    
    def interrogate_suspects(self):
        self.clear_screen()
        self.print_header("ДОПРОС ПОДОЗРЕВАЕМЫХ")
        
        not_questioned = [s for s, info in self.suspects.items() if not info['допрошена']]
        
        if not not_questioned:
            self.slow_print("Вы уже допросили всех подозреваемых.")
            return
        
        self.slow_print("Кого вы хотите допросить?")
        
        suspect_list = list(not_questioned)
        suspect_list.append("Вернуться позже")
        
        choice = self.choice_maker(suspect_list)
        
        if choice <= len(not_questioned):
            suspect = suspect_list[choice - 1]
            self.interrogate(suspect)
    
    def interrogate(self, suspect):
        self.clear_screen()
        self.print_header(f"ДОПРОС: {suspect}")
        
        self.suspects[suspect]['допрошена'] = True
        
        if suspect == "Мираэль (эльфийка-артефактор)":
            self.interrogate_mirael()
        elif suspect == "Боргар (гном-алхимик)":
            self.interrogate_borgar()
        elif suspect == "Селен (человек-библиотекарь)":
            self.interrogate_selen()
        elif suspect == "Верховный маг Аргус":
            self.slow_print("Но он же мертв! Вы не можете его допросить.")
            self.suspects[suspect]['допрошена'] = False
    
    def interrogate_mirael(self):
        self.slow_print("Мираэль встречает вас с холодным спокойствием.")
        self.slow_print("Она - лучший артефактор гильдии, известная своим высокомерием.")
        
        self.slow_print("\nМираэль: \"Я знаю, зачем вы пришли. Думаете, это я убила старика?\"")
        
        options = [
            "Где вы были в момент убийства?",
            "Почему вас могли подозревать?",
            "Что вы знаете о заколке, найденной на месте преступления? (если есть)",
            "Покажите ваши руки (проверка на следы)",
            "Закончить допрос"
        ]
        
        interrogating = True
        while interrogating:
            choice = self.choice_maker(options)
            
            if choice == 1: 
                self.slow_print("\nМираэль: \"Я была в своей лаборатории, работала над новым артефактом.")
                self.slow_print("Мой ученик может подтвердить - он приносил мне обед около полудня.\"")
                self.suspects['Мираэль (эльфийка-артефактор)']['алиби'] = "Ученик подтверждает"
                
                if self.charisma >= 60:
                    self.slow_print("\nВы чувствуете фальшь в ее голосе. Она что-то недоговаривает.")
                    self.clues.append("Мираэль нервничает при вопросе об алиби")
                    self.update_stats(perception=5)
            
            elif choice == 2:  
                self.slow_print("\nМираэль: \"У нас были разногласия по поводу исследований.")
                self.slow_print("Аргус считал мои эксперименты опасными и хотел закрыть мою лабораторию.\"")
                self.clues.append("Мираэль имела конфликт с жертвой")
            
            elif choice == 3 and self.inventory['заколка эльфийки']:  
                self.slow_print("\nВы показываете заколку Мираэль.")
                self.slow_print("Она бледнеет: \"Это... это моя заколка. Я потеряла ее несколько дней назад.")
                self.slow_print("Должно быть, она выпала, когда я заходила к Аргусу обсудить дела.\"")
                
                if self.logic >= 55:
                    self.slow_print("\nВы замечаете, что она слишком быстро нашла объяснение.")
                    self.slow_print("Будто заранее придумала эту историю.")
                    self.clues.append("Мираэль подозрительно быстро объяснила наличие заколки")
                    self.update_stats(logic=5)
            
            elif choice == 4: 
                self.slow_print("\nМираэль неохотно показывает руки.")
                if self.perception >= 55:
                    self.slow_print("Вы замечаете свежие царапины на ее запястьях.")
                    self.slow_print("Похоже на следы от когтей или магической защиты.")
                    self.clues.append("Царапины на руках Мираэль")
                else:
                    self.slow_print("Руки чистые, без следов борьбы.")
            
            else:
                interrogating = False
    
    def interrogate_borgar(self):
        self.slow_print("Боргар - старый гном-алхимик, который вечно ворчит.")
        self.slow_print("Он варит зелья в своей лаборатории и никому не доверяет.")
        
        self.slow_print("\nБоргар: \"Кого принесло? Опять допрос? Я ничего не знаю!\"")
        
        options = [
            "Где вы были?",
            "Что вы знаете о ядах?",
            "Покажите ваши ингредиенты",
            "Что за порошок найден на месте преступления? (если есть)",
            "Закончить допрос"
        ]
        
        interrogating = True
        while interrogating:
            choice = self.choice_maker(options)
            
            if choice == 1:  
                self.slow_print("\nБоргар: \"Я был в подвале, перебирал ингредиенты.")
                self.slow_print("Стражник видел меня, когда приносил обед в подвал.\"")
                self.suspects['Боргар (гном-алхимик)']['алиби'] = "Стражник подтверждает"
            
            elif choice == 2:  
                self.slow_print("\nБоргар: \"Я знаю о ядах всё! Это моя специальность.")
                self.slow_print("Аргус часто просил меня приготовить редкие составы для его экспериментов.\"")
                
                if self.inventory['странный порошок']:
                    self.slow_print("\nВы показываете найденный порошок.")
                    self.slow_print("Боргар внимательно изучает его:")
                    self.slow_print("\"Это редкий эльфийский яд из Черного Леса.")
                    self.slow_print("Очень дорогой и смертоносный. Я сам его не варю.\"")
                    self.clues.append("Яд эльфийского происхождения")
                    self.update_stats(logic=5)
            
            elif choice == 3:  
                self.slow_print("\nБоргар ведет вас к своим запасам.")
                if self.perception >= 65:
                    self.slow_print("Среди обычных ингредиентов вы замечаете пузырек с таким же порошком!")
                    self.slow_print("Боргар смущается: \"Э-э... это я для исследования взял.\"")
                    self.clues.append("У Боргара найден такой же яд")
                else:
                    self.slow_print("Все ингредиенты выглядят обычно для лаборатории алхимика.")
            
            elif choice == 4 and self.inventory['странный порошок']:  
                self.slow_print("\nВы показываете порошок Боргару.")
                self.slow_print("Он мрачнеет: \"Это эльфийская отрава. Редкая штука.")
                self.slow_print("В гильдии только у меня и у Мираэль могли быть такие компоненты.\"")
                self.clues.append("Яд могли иметь только алхимик или эльфийка")
            
            else:
                interrogating = False
    
    def interrogate_selen(self):
        self.slow_print("Селен - тихий молодой человек, работающий в библиотеке гильдии.")
        self.slow_print("Он очень нервничает, когда вы к нему подходите.")
        
        self.slow_print("\nСелен: \"О-о, детектив... Я... я ничего не знаю, честно!\"")
        
        options = [
            "Успокойтесь и расскажите, где вы были",
            "Почему вы так нервничаете?",
            "Что вы видели?",
            "Покажите ваши вещи",
            "Закончить допрос"
        ]
        
        interrogating = True
        while interrogating:
            choice = self.choice_maker(options)
            
            if choice == 1:  
                self.slow_print("\nСелен: \"Я... я был в библиотеке всё утро.")
                self.slow_print("Приходил ученик Мираэль за книгой, он может подтвердить.\"")
                self.suspects['Селен (человек-библиотекарь)']['алиби'] = "Ученик подтверждает"
            
            elif choice == 2: 
                if self.charisma >= 50:
                    self.slow_print("\nВы мягко убеждаете его успокоиться.")
                    self.slow_print("Селен: \"Я... я видел кое-что. Но боюсь говорить.")
                    self.slow_print("Если узнают, что я рассказал...\"")
                    self.clues.append("Селен что-то скрывает")
                else:
                    self.slow_print("\nСелен: \"Я просто боюсь! Здесь убийца, а вы меня допрашиваете!\"")
            
            elif choice == 3:  
                if self.charisma >= 55 or 'Селен что-то скрывает' in self.clues:
                    self.slow_print("\nСелен оглядывается и шепчет:")
                    self.slow_print("\"Я видел, как Мираэль выходила из лаборатории Аргуса поздно вечером.")
                    self.slow_print("Она была очень бледна и прятала руки в карманах.\"")
                    self.clues.append("Свидетель видел Мираэль у лаборатории")
                else:
                    self.slow_print("\nСелен: \"Ничего особенного. Все как обычно.\"")
            
            elif choice == 4:  
                self.slow_print("\nВы просите показать содержимое карманов.")
                if self.perception >= 50:
                    self.slow_print("Среди книг вы замечаете платок со следами крови!")
                    self.slow_print("Селен в панике: \"Это не то, что вы думаете! Я порезался бумагой!\"")
                    
                    take_handkerchief = self.choice_maker(["Взять платок как улику", "Поверить ему"])
                    if take_handkerchief == 1:
                        self.inventory['кровь на платке'] = True
                        self.clues.append("Кровавый платок Селена")
                        self.suspects['Селен (человек-библиотекарь)']['алиби'] = "Подозрительно"
                else:
                    self.slow_print("Ничего подозрительного, только книги и бумаги.")
            
            else:
                interrogating = False
    
    def analyze_evidence(self):
        self.clear_screen()
        self.print_header("АНАЛИЗ УЛИК")
        
        if not self.clues:
            self.slow_print("У вас пока нет улик для анализа.")
            self.slow_print("Вернитесь на место преступления и соберите больше доказательств.")
            return
        
        self.slow_print("Вы раскладываете все собранные улики на столе.")
        self.show_inventory()
        
        self.slow_print("\nЧто вы хотите проанализировать?")
        
        clue_list = self.clues.copy()
        clue_list.append("Закончить анализ")
        
        choice = self.choice_maker(clue_list)
        
        if choice <= len(self.clues):
            clue = clue_list[choice - 1]
            self.analyze_clue(clue)
        else:
            return
    
    def analyze_clue(self, clue):
        self.slow_print(f"\nВы внимательно изучаете: {clue}")
        
        if "Дневник" in clue and self.inventory['дневник жертвы']:
            self.slow_print("В дневнике Аргуса вы находите важные записи:")
            self.slow_print("• Конфликт с Мираэль по поводу опасных экспериментов")
            self.slow_print("• Боргар требовал больше денег за редкие ингредиенты")
            self.slow_print("• Селен боялся, что его уволят за потерю древней книги")
            self.slow_print("• Аргус подозревал, что кто-то ворует магические артефакты")
            self.update_stats(logic=10)
        
        elif "кинжал" in clue and self.inventory['отравленный кинжал']:
            if self.logic >= 50:
                self.slow_print("Вы изучаете кинжал. На рукоятке эльфийские символы.")
                self.slow_print("Лезвие отравлено - экспертиза покажет, тем же ли ядом.")
                self.clues.append("Кинжал эльфийской работы")
            else:
                self.slow_print("Обычный кинжал. Нужен эксперт по ядам.")
        
        elif "порошок" in clue and self.inventory['странный порошок']:
            self.slow_print("Вы рассматриваете порошок через увеличительное стекло.")
            if self.logic >= 60 or self.class_type == "Маг":
                self.slow_print("Это редкий эльфийский яд 'Слеза Дриады'.")
                self.slow_print("Смертелен при попадании в кровь. Действует мгновенно.")
                self.clues.append("Яд редкий, доступен не каждому")
        
        elif "заколка" in clue:
            self.slow_print("Эльфийская заколка высокого качества.")
            self.slow_print("Такие носят только знатные эльфы. Мираэль знатного рода.")
        
        elif "царапины" in clue:
            self.slow_print("Царапины на руках Мираэль...")
            self.slow_print("Они похожи на следы от магической защиты, которую ставил Аргус.")
            self.slow_print("Значит, она была близко к нему в момент смерти.")
        
        elif "кровь" in clue and self.inventory['кровь на платке']:
            self.slow_print("Кровь на платке еще свежая.")
            self.slow_print("Нужно проверить, принадлежит ли она жертве.")
        
        input("\nНажмите Enter, чтобы продолжить...")
    
    def final_accusation(self):
        self.clear_screen()
        self.print_header("ФИНАЛЬНОЕ ОБВИНЕНИЕ")
        
        self.slow_print("Вы собрали все улики и готовы назвать убийцу.")
        self.slow_print("Совет Гильдии собрался в главном зале.")
        self.slow_print("Все подозреваемые здесь. Напряжение растет...")
        
        self.print_separator()
        self.slow_print("Кого вы обвините в убийстве Верховного мага Аргуса?")
        
        suspect_names = list(self.suspects.keys())
        suspect_names.append("Я не готов (вернуться к расследованию)")
        
        choice = self.choice_maker(suspect_names)
        
        if choice <= 4:
            accused = suspect_names[choice - 1]
            return self.present_case(accused)
        else:
            return False
    
    def present_case(self, accused):
        self.clear_screen()
        self.print_header(f"ОБВИНЕНИЕ: {accused}")
        
        self.slow_print("Вы выходите вперед и указываете на подозреваемого:")
        self.slow_print(f'"Убийца - {accused}!"')
        
        evidence_count = len(self.clues)
        
        if evidence_count < 3:
            self.slow_print("\nВ зале поднимается шум. Ваши обвинения звучат неубедительно.")
            self.slow_print("У вас слишком мало улик, чтобы доказать вину.")
            self.bad_ending("Недостаточно улик")
            return True
        
        conviction_score = 0
        needed_score = 3
        
        if accused == "Мираэль (эльфийка-артефактор)":
            if "Эльфийская заколка" in str(self.clues):
                conviction_score += 1
                self.slow_print("✓ Заколка Мираэль найдена на месте преступления")
            if "Царапины на руках Мираэль" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Царапины от магической защиты жертвы")
            if "Свидетель видел Мираэль у лаборатории" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Свидетель видел ее у лаборатории")
            if "Яд эльфийского происхождения" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Использован эльфийский яд")
            if "Кинжал эльфийской работы" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Орудие убийства эльфийской работы")
        
        elif accused == "Боргар (гном-алхимик)":
            if "У Боргара найден такой же яд" in self.clues:
                conviction_score += 2
                self.slow_print("✓ У подозреваемого найден такой же яд")
            if "Книга о ядах" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Книга о ядах была открыта")
            if "Отравленный кинжал" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Орудие убийства - отравлен")
        
        elif accused == "Селен (человек-библиотекарь)":
            if "Кровавый платок Селена" in self.clues:
                conviction_score += 1
                self.slow_print("✓ У подозреваемого найден окровавленный платок")
            if "Селен что-то скрывает" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Подозреваемый ведет себя подозрительно")
            if "Подозрительные письма" in self.clues:
                conviction_score += 1
                self.slow_print("✓ Найдены письма о шантаже")
        
        self.slow_print(f"\nУлик против обвиняемого: {conviction_score}/{needed_score}")
        
        if conviction_score >= needed_score:
            self.slow_print("\nВаши доказательства неопровержимы!")
            self.slow_print("Подозреваемый ломается и признается в убийстве...")
            self.good_ending(accused)
        else:
            self.slow_print("\nУлик недостаточно. Подозреваемый все отрицает.")
            self.slow_print("Без веских доказательств вы не можете доказать вину.")
            self.bad_ending("Недостаточно улик против конкретного подозреваемого")
        
        return True
    
    def good_ending(self, accused):
        self.clear_screen()
        self.print_header("ПРАВОСУДИЕ ВОСТОРЖЕСТВОВАЛО")
        
        if "Мираэль" in accused:
            self.slow_print("Мираэль признается в убийстве на почве мести.")
            self.slow_print("Аргус хотел закрыть ее лабораторию и лишить ее жизненного дела.")
            self.slow_print("Она подсыпала яд в вино и добила кинжалом, когда яд начал действовать.")
        elif "Боргар" in accused:
            self.slow_print("Боргар признается, что убил Аргуса из-за денег.")
            self.slow_print("Аргус задолжал ему крупную сумму за редкие ингредиенты.")
            self.slow_print("Гном не выдержал и отравил старого мага.")
        else:
            self.slow_print("Селен признается, что его шантажировали.")
            self.slow_print("Кто-то узнал о его темных делах и заставил убить Аргуса.")
            self.slow_print("Но он отказывается называть имя заказчика...")
        
        self.slow_print(f"\nГильдия благодарит вас, детектив {self.player_name}!")
        self.slow_print("Вас награждают титулом Почетного детектива Гильдии Магов.")
        self.slow_print("Ваше имя войдет в историю Эренделла!")
        
        self.murder_solved = True
        self.ending = "good"
        
        return True
    
    def bad_ending(self, reason):
        self.clear_screen()
        self.print_header("ПРОВАЛ РАССЛЕДОВАНИЯ")
        
        if reason == "Недостаточно улик":
            self.slow_print("Совет Гильдии не удовлетворен вашей работой.")
            self.slow_print("Без достаточных улик дело остается нераскрытым.")
            self.slow_print("Убийца так и не найден. Страх продолжает жить в стенах гильдии.")
        else:
            self.slow_print("Вы обвинили не того человека.")
            self.slow_print("Настоящий убийца остается на свободе.")
            self.slow_print("А невиновный страдает из-за вашей ошибки.")
        
        self.slow_print(f"\nВаша репутация детектива {self.player_name} разрушена.")
        self.slow_print("Вам предлагают покинуть гильдию и забыть об этом деле.")
        
        self.ending = "bad"
        
        return True
    
    def secret_ending(self):
        self.clear_screen()
        self.print_header("ТАЙНА РАСКРЫТА")
        
        self.slow_print("Вы понимаете, что все не так просто...")
        self.slow_print("Амулет, найденный в тайнике, принадлежит тайной организации 'Черный Совет'.")
        self.slow_print("Аргус был их агентом, но решил выйти из игры.")
        self.slow_print("Его убили свои же, чтобы сохранить тайну.")
        
        self.slow_print("\nВы стоите перед выбором:")
        secret_choice = self.choice_maker([
            "Обнародовать правду (опасно для жизни)",
            "Сжечь улики и уехать из города",
            "Попытаться внедриться в Черный Совет"
        ])
        
        if secret_choice == 1:
            self.slow_print("\nВы публикуете расследование. Черный Совет в ярости.")
            self.slow_print("Вас пытаются убить, но вы слишком хороший детектив.")
            self.slow_print("Совет магов объявляет войну тайной организации.")
            self.slow_print("Начинается магическая война, а вы - ее герой!")
        elif secret_choice == 2:
            self.slow_print("\nВы сжигаете все улики и уезжаете на рассвете.")
            self.slow_print("Никто не узнает правду, но вы останетесь живы.")
            self.slow_print("Где-то далеко вы начинаете новую жизнь...")
        else:
            self.slow_print("\nВы решаете играть по-крупному.")
            self.slow_print("Внедрившись в Черный Совет, вы становитесь двойным агентом.")
            self.slow_print("Кто знает, к чему приведет эта опасная игра?")
        
        self.ending = "secret"
        
        return True
    
    def game_loop(self):
        while not self.game_over and not self.murder_solved:
            self.clear_screen()
            self.print_header("ЧТО ДЕЛАЕМ?")
            
            options = [
                "Осмотреть место преступления",
                "Допросить подозреваемых",
                "Проанализировать улики",
                "Показать статус и инвентарь",
                "Выдвинуть обвинение"
            ]
            
            choice = self.choice_maker(options)
            
            if choice == 1:
                self.investigate_crime_scene()
            elif choice == 2:
                self.interrogate_suspects()
            elif choice == 3:
                self.analyze_evidence()
            elif choice == 4:
                self.show_stats()
                self.show_inventory()
                self.show_suspects_status()
                input("\nНажмите Enter, чтобы продолжить...")
            elif choice == 5:
                if self.final_accusation():
                    break
            
            if self.inventory['магический амулет'] and len(self.clues) >= 5 and self.logic >= 70:
                secret_trigger = random.randint(1, 100)
                if secret_trigger > 80:  # 20% шанс найти секретную концовку
                    self.secret_ending()
                    break
    
    def play(self):
        self.clear_screen()
        self.print_header("ТЕНЬ ЧЕРНОГО ЛЕСА")
        self.slow_print("Детектив в мире фэнтези")
        time.sleep(1.5)
        
        self.create_character()
        self.prologue()
        self.game_loop()
        
        self.print_separator()
        if self.ending == "good":
            self.slow_print(" ПОБЕДА! Вы раскрыли преступление!")
        elif self.ending == "secret":
            self.slow_print(" СЕКРЕТНАЯ КОНЦОВКА! Вы узнали правду!")
        else:
            self.slow_print(" ПОРАЖЕНИЕ... Попробуйте еще раз!")
        
        self.print_separator()
        self.slow_print("Спасибо за игру!")
        input("\nНажмите Enter для выхода...")

def main():
    game = FantasyDetective()
    game.play()

if __name__ == "__main__":
    main()