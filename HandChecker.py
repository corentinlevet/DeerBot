from WindowCapture import WindowCapture
import numpy as np
from PIL import Image
import os
from Card import Card, CardType

class HandChecker:
    HERO_CONFIG = {
        "Thor": {"color": "blue", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}},
        "Albedo": {"color": "blue", "cards": {"1": CardType.MALUS, "2": CardType.COUNTER, "Ult": CardType.ULTIMATE}},
        "Jörmungand": {"color": "green", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}},
        "Freyr": {"color": "red", "cards": {"1": CardType.ATTACK, "2": CardType.ATTACK, "Ult": CardType.ULTIMATE}}
    }

    def __init__(self):
        self.regions = [
            {"top": 974, "left": 1232, "width": 50, "height": 50},
            {"top": 974, "left": 1318, "width": 50, "height": 50},
            {"top": 974, "left": 1404, "width": 50, "height": 50},
            {"top": 974, "left": 1490, "width": 50, "height": 50},
            {"top": 974, "left": 1576, "width": 50, "height": 50},
            {"top": 974, "left": 1662, "width": 50, "height": 50},
            {"top": 974, "left": 1748, "width": 50, "height": 50},
            {"top": 974, "left": 1834, "width": 50, "height": 50},
        ]

    def create_card(self, hero, card_name, index):
        if hero not in self.HERO_CONFIG:
            raise Exception(f"Héros non reconnu: {hero}.")

        hero_config = self.HERO_CONFIG[hero]
        if card_name not in hero_config["cards"]:
            raise Exception(f"Carte non reconnue pour {hero}: {card_name}.")

        card_type = hero_config["cards"][card_name]
        color = hero_config["color"]
        return Card(hero, color, card_type, index)

    def get_filtered_cards(self, skills_array):
        cards = []

        for i, skill in enumerate(skills_array):
            hero, card_name = skill.split("_")
            card = self.create_card(hero, card_name, i + 1)
            cards.append(card)

        return cards

    def are_images_equal(self, img1_path, img2_path):
        # Charger les images
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        # Vérifier si les tailles des images sont différentes
        if img1.size != img2.size:
            return False

        # Convertir les images en tableaux numpy pour une comparaison efficace
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)

        # On boucle sur chaque ligne puis chaque pixel de chaque ligne, et on fait une incertitude de 10
        good_pixels = 0
        for i in range(np_img1.shape[0]):
            for j in range(np_img1.shape[1]):
                for k in range(np_img1.shape[2]):
                    res = np_img1[i, j, k] - np_img2[i, j, k]
                    res = abs(res)
                    if res > 60:
                        pass
                    else:
                        good_pixels += 1

        # On calcule le pourcentage de pixels identiques
        percentage = good_pixels / (np_img1.shape[0] * np_img1.shape[1] * np_img1.shape[2])
        # if percentage > 0.5:
        #     print(f"Pourcentage de pixels identiques: {round(percentage * 100, 2)}%")

        return percentage > 0.5

    def get_hand(self):
        # Prendre une capture de chaque région de la main
        wc = WindowCapture("7DS")
        for i, region in enumerate(self.regions):
            wc.capture(f"Hand/{i}", region)

        # Comparer chaque région avec les cartes de compétences
        skills_folder = "Skills"
        skills = os.listdir(skills_folder)
        # Virer ce qui n'est pas une image
        skills = [skill for skill in skills if skill.endswith(".png")]

        skills_array = []

        for i in range(len(self.regions)):
            for skill in skills:
                hand_str = f"Hand/{i}.png"
                skill_str = f"{skills_folder}/{skill}"
                # print(f"Comparing {hand_str} with {skill_str}")
                if self.are_images_equal(hand_str, skill_str):
                    skills_array.append(skill.split(".")[0])
                    break
            else:
                raise Exception(f"Carte non reconnue pour la région {i}.")

        return skills_array

    def print_hand(self, cards):
        for card in cards:
            print(card)
