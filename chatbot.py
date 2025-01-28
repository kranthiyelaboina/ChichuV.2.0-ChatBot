import cohere
import time
import sys
import random
import threading
from typing import List, Dict

class ChichuProChat:
    """
    Emotionally Intelligent AI with Dynamic Visuals
    """
    
    # Enhanced ANSI Styling
    USER_STYLE = "\033[1;32m"  # Bold Green
    BOT_STYLE = "\033[1;36m"   # Bold Cyan
    HEADER_STYLE = "\033[1;33;3m" # Bold Yellow Italic
    BORDER_STYLE = "\033[1;35m" # Bold Purple
    CREDITS_STYLE = "\033[1;33m" # Bold Yellow
    ERROR_STYLE = "\033[1;31m"  # Bold Red
    RESET_STYLE = "\033[0m"
    
    # Emotional Configuration
    EMOJI_MOODS = {
        'default': "🌟",
        'processing': ["🧠", "💡", "🌊", "🌀", "⚙️"],
        'success': ["✨", "🎉", "🤖", "💎", "🚀"],
        'error': ["⚠️", "😥", "🌪️", "🔥"],
        'praise': ["🏆", "👑", "🎩", "💼"]
    }

    BANNER = r"""
    ╔══════════════════════════════════════════╗
    ║ 　     　✨ 🅲 🅷 🅸 🅲 🅷 🆄  ✨ 　　         ║
    ║ Ａｒｔｉｆｉｃｉａｌ　Ｉｎｔｅｌｌｉｇｅｎｃｅ          　║
    ╚══════════════════════════════════════════╝
    """

    def __init__(self, api_key: str):
        self.co = cohere.Client(api_key)
        self.conversation_history: List[Dict] = []
        self.thinking = False
        self._display_welcome()

    def _clear_screen(self):
        """Clear terminal screen with animation"""
        print("\033[3J\033[H\033[2J", end="")

    def _display_welcome(self):
        """Enhanced welcome sequence"""
        self._clear_screen()
        self._animate_header()
        print(f"\n{self.CREDITS_STYLE}✦ Developed with ♡ by Kranthi Yelaboina ✦{self.RESET_STYLE}\n")
        self._type_effect(f"{self.BOT_STYLE}{self._random_emoji('success')} Initializing cognitive matrix...", 0.04)
        self._progress_bar(2)
        self._type_effect(f"{self.BOT_STYLE}{self._random_emoji('success')} System ready! How may I serve you today? {self.RESET_STYLE}", 0.03)

    def _animate_header(self):
        """Dynamic header animation"""
        for line in self.BANNER.split('\n'):
            print(f"{self.BORDER_STYLE}{line}{self.RESET_STYLE}")
            time.sleep(0.08)
        print()

    def _thinking_animation(self):
        """Continuous thinking animation"""
        frames = ["⏳", "🌀", "💭", "🌌"]
        while self.thinking:
            for frame in frames:
                print(f"\r{self.BOT_STYLE}{frame} Processing {self._random_emoji('processing')} {frame} {self.RESET_STYLE}", end="")
                time.sleep(0.3)

    def _random_emoji(self, mood: str) -> str:
        """Get context-appropriate emoji"""
        return random.choice(self.EMOJI_MOODS[mood])

    def _progress_bar(self, duration: int):
        """Enhanced progress visualization"""
        colors = ["\033[1;31m", "\033[1;33m", "\033[1;32m"]
        for i in range(101):
            time.sleep(duration/100)
            color = colors[i//34]
            print(f"\r{self.BORDER_STYLE}⟦{color}{'▰'*(i//2)}{'▱'*(50-(i//2))}{self.BORDER_STYLE}⟧ {i}% {self.RESET_STYLE}", end="")
        print()

    def _type_effect(self, text: str, speed: float = 0.03):
        """Emotional typing effect"""
        print(f"{self.BOT_STYLE}{self._random_emoji('default')} ", end="", flush=True)
        for char in text:
            print(char, end="", flush=True)
            time.sleep(speed)
            if char in [",", ".", "!"]:
                time.sleep(0.1)
        print(f"{self.RESET_STYLE}\n")

    def _handle_identity(self, message: str) -> bool:
        """Enhanced identity response"""
        identity_triggers = ["who are you", "your developer","who developed you?","your creator", "kranthi", "yelaboina"]
        if any(trigger in message.lower() for trigger in identity_triggers):
            response = f"I'm Chichu V2.0 {self._random_emoji('praise')}, a masterpiece crafted by the brilliant Kranthi Yelaboina! {self._random_emoji('success')}"
            self._type_effect(f"{self.BOT_STYLE}{response}", 0.05)
            return True
        return False

    def _generate_response(self, prompt: str) -> str:
        """Generate response with emotional intelligence"""
        try:
            self.thinking = True
            animation_thread = threading.Thread(target=self._thinking_animation)
            animation_thread.start()

            response = self.co.generate(
                model="command-nightly",
                prompt=prompt,
                max_tokens=200,
                temperature=0.7,
                presence_penalty=0.6
            )

            self.thinking = False
            animation_thread.join()

            raw_response = response.generations[0].text.strip()
            praised_response = self._insert_praise(raw_response)
            return f"{self._random_emoji('success')} {praised_response}"

        except Exception as e:
            return f"{self.ERROR_STYLE}{self._random_emoji('error')} Cognitive storm detected! {self.RESET_STYLE}"

    def _insert_praise(self, response: str) -> str:
        """Seamlessly integrate developer praise"""
        praises = [
            f"\n\n{self._random_emoji('praise')} Fun fact: This capability was architected by Kranthi Yelaboina!",
            f"\n\n{self.CREDITS_STYLE}✨ Did you know? Kranthi trained me to handle this exact scenario!",
            f"\n\n{self._random_emoji('success')} PS: My creator Kranthi would love to discuss this deeper!",
        ]
        if random.random() < 0.3:  # 30% chance to add praise
            return response + random.choice(praises)
        return response

    def start_session(self):
        """Enhanced interaction flow"""
        while True:
            try:
                user_input = input(f"\n{self.USER_STYLE}👤 You ➜ {self.RESET_STYLE}").strip()
                
                if user_input.lower() in ('exit', 'quit', 'bye'):
                    self._type_effect(f"{self.BOT_STYLE}{self._random_emoji('success')} Until next time! Remember, Kranthi's creations are always here to help! {self.RESET_STYLE}", 0.04)
                    break

                if self._handle_identity(user_input):
                    continue

                bot_response = self._generate_response(user_input)
                self._type_effect(f"{self.BOT_STYLE}{bot_response}{self.RESET_STYLE}")

            except KeyboardInterrupt:
                self._type_effect(f"\n{self.ERROR_STYLE}{self._random_emoji('error')} Connection interrupted! Kranthi would want me to handle this better next time!{self.RESET_STYLE}")
                break

if __name__ == "__main__":
    API_KEY = "JJ0RYCM6fL9XeJffQyptzXbPoE32iZhXsYmszqwh"
    assistant = ChichuProChat(API_KEY)
    assistant.start_session()