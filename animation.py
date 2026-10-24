# ==========================================
# ЧАСТЬ 1: Математическая модель и генерация галактики
# ==========================================
class GalaxyTopology:
    def __init__(self, scale, cx, cy):
        self.scale = scale
        self.cx = cx
        self.cy = cy
        self.bar_angle = math.radians(-30)
        self.galaxy_branches = []
        self.galaxy_stars = []
        self.sky_stars = []
        self.core_particles = []
        self.back_rings = []
        self.front_rings = []
        self.bottom_rings = []

    def get_gradient_color(self, t):
        if t < 0.12: return "#F0F8FF"
        if t < 0.35: return f"#{int(240 - 40*t/0.35):02x}{int(248 - 65*t/0.35):02x}ff"
        if t < 0.70: p = (t - 0.35) / 0.35; return f"#{int(190 - 150*p):02x}{int(212 - 140*p):02x}ff"
        return f"#{int(40 - 40*((t - 0.70)/0.30)):02x}{int(72 - 60*((t - 0.70)/0.30)):02x}{int(255 - 180*((t - 0.70)/0.30)):02x}"

    def build(self, canvas, logo_r, bar_offset):
        pool = ["#FFFFFF"] * 12 + ["#FFD54F"] * 5 + ["#64B5F6"] * 3
        max_bg_dist = 280 * self.scale
        
        for _ in range(200):
            ang, dist, col = random.uniform(0, 2*math.pi), random.uniform(0, max_bg_dist), random.choice(pool)
            x, y = self.cx + dist * math.cos(ang), self.cy + dist * math.sin(ang)
            self.sky_stars.append({
                "id": canvas.create_oval(x, y, x + 2, y + 2, fill=col, outline=""), 
                "blink_speed": random.uniform(0.05, 0.12), "blink_phase": random.uniform(0, 10), "base_color": col
            })
            
        for i in range(140):
            arm_phase, is_milk, segments = (i * 2 * math.pi) / 140, (i % 4 == 0), []
            for j in range(40):
                t_seg = j / 40
                color = "#F0F8FF" if is_milk and t_seg < 0.35 else (f"#{int(240 - 35*(t_seg/0.7)):02x}{int(248 - 50*(t_seg/0.7)):02x}ff" if is_milk else self.get_gradient_color(t_seg))
                w_max, w_min = (6.0 * self.scale, 2.5 * self.scale) if is_milk else (4.5 * self.scale, 1.5 * self.scale)
                width_val = max(w_min, w_max * (1.0 - t_seg * (0.5 if is_milk else 0.7)))
                segments.append(canvas.create_line(0, 0, 0, 0, fill=color, width=width_val, capstyle="round"))
                
            branch_data = {"segments": segments, "phase": arm_phase, "r_max": (195 + (i % 3) * 12) * self.scale, "is_milk": is_milk}
            self.galaxy_branches.append(branch_data)
            for _ in range(16 if is_milk else 5):
                t_star = random.uniform(0.01, 1.0)
                self.galaxy_stars.append({
                    "id": canvas.create_oval(0, 0, 0, 0, fill=random.choice(pool) if (is_milk or random.random() > 0.4) else self.get_gradient_color(t_star), outline=""), 
                    "branch": branch_data, "t": t_star, "size": random.choice([1, 2, 2]) * self.scale
                })
        
        cols = ["#1f0700", "#381001", "#541902", "#732403", "#913004", "#b03e05", "#cf4d06", "#ed5e08", "#ff7311", "#ff8624", "#ff9b3b", "#ffb154", "#ffc670", "#ffd98c", "#ffe9a6", "#fff4c2", "#fffada", "#ffffff"]
        for idx in range(70):
            thick_cfg = {"fill": cols[min(idx // 4, 17)], "width": max(0.25 * self.scale, (1.3 - idx * 0.015) * self.scale), "capstyle": "round", "state": "hidden"}
            front_cfg = {"fill": cols[min(idx // 4, 17)], "width": max(1.5 * self.scale, (6.0 - idx * 0.07) * self.scale), "capstyle": "round", "state": "hidden"}
            
            r_outer = (95 + idx * 0.6) * self.scale
            r_front = (68 + idx * 0.4) * self.scale
            
            self.back_rings.append({"id": canvas.create_line(0, 0, 0, 0, **thick_cfg), "base_r": r_outer})
            self.bottom_rings.append({"id": canvas.create_line(0, 0, 0, 0, **thick_cfg), "base_r": r_outer})
            self.front_rings.append({"id": canvas.create_line(0, 0, 0, 0, **front_cfg), "base_r": r_front})

        for _ in range(800):
            ang, dist = random.uniform(0, 2 * math.pi), random.uniform(0, 1.0) ** 1.6
            self.core_particles.append({
                "id": canvas.create_oval(0, 0, 0, 0, fill=random.choice(["#FFFFFF", "#FFFDE7"]) if dist < 0.35 else random.choice(["#FFF9C4", "#FFF59D"]), outline=""), 
                "local_x": 45 * self.scale * dist * math.cos(ang), "local_y": 18 * self.scale * dist * math.sin(ang), 
                "branch": random.choice(self.galaxy_branches), "t_factor": dist * 0.15
            })

    def sample_spiral_path(self, t, branch, progress, frame, logo_r, bar_offset):
        r_space = t * branch["r_max"]
        angle_vortex = self.bar_angle + branch["phase"] + 6.8 * (t ** 0.5) + (frame * 0.10) + ((35 * self.scale) / (r_space + 12 * self.scale)) * progress
        if branch["phase"] < math.pi / 2 or (math.pi <= branch["phase"] < 3 * math.pi / 2):
            tx = self.cx - 100 * self.scale + t * 200 * self.scale
            ty = self.cy - bar_offset if branch["phase"] < math.pi else self.cy + bar_offset
        else:
            tx = self.cx + logo_r * math.cos(self.bar_angle + branch["phase"] + t * 2 * math.pi)
            ty = self.cy + logo_r * math.sin(self.bar_angle + branch["phase"] + t * 2 * math.pi)
        sp = progress * progress * (3.0 - 2.0 * progress)
        return (1.0 - sp) * (self.cx + r_space * math.cos(angle_vortex)) + sp * tx, (1.0 - sp) * (self.cy + r_space * math.sin(angle_vortex)) + sp * ty

# ==========================================
# ЧАСТЬ 2: Адаптивное окно и гравитационные кольца
# ==========================================
class ElegantGalacticTransform:
    def __init__(self, root):
        self.root = root
        root.wm_attributes("-transparentcolor", "#00FF00", "-topmost", True)
        root.overrideredirect(True)
        
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        self.base_size = min(sw, sh) // 4
        
        x_pos = (sw - self.base_size) // 2
        y_pos = (sh - self.base_size) // 2
        root.geometry(f"{self.base_size}x{self.base_size}+{x_pos}+{y_pos}")
        
        self.canvas = Canvas(root, width=self.base_size, height=self.base_size, bg="#00FF00", highlightthickness=0)
        self.canvas.pack()
        
        self.scale = self.base_size / 600.0
        self.cx = self.cy = self.base_size // 2
        self.frame = 0
        
        self.logo_r = 185 * self.scale
        self.bar_offset = 48 * self.scale
        
        self.topo = GalaxyTopology(self.scale, self.cx, self.cy)
        self.topo.build(self.canvas, self.logo_r, self.bar_offset)
        
        self.shadow_id = self.canvas.create_oval(0, 0, 0, 0, fill="#000000", outline="", state="hidden")
        self.logo_circle = self.canvas.create_oval(0, 0, 0, 0, outline="#F0F8FF", width=12 * self.scale, state="hidden")
        self.logo_bar1 = self.canvas.create_line(0, 0, 0, 0, fill="#F0F8FF", width=44 * self.scale, capstyle="round", state="hidden")
        self.logo_bar2 = self.canvas.create_line(0, 0, 0, 0, fill="#F0F8FF", width=44 * self.scale, capstyle="round", state="hidden")
        
        self.flare_elements = []
        self.flare_frame = 0
        self.flare_triggered = False  # Контроль однократного запуска вспышки
        
        self.animate()

    def draw_lensed_rings(self, rings, wave, dy, mode):
        for ring in rings:
            self.canvas.itemconfigure(ring["id"], state="normal")
            r, pts = ring["base_r"] * wave, []
            for step in range(41):
                ang = -math.pi + (step / 40) * 2 * math.pi
                cos_val, sin_val = math.cos(ang), math.sin(ang)
                is_behind = (sin_val < 0)
                
                zoom_x = 1.45
                target_x = self.cx + r * cos_val * zoom_x
                
                tight_pinch = sin_val * sin_val
                round_dome = math.pow(abs(sin_val), 1.85) * tight_pinch
                
                if mode == "back" and is_behind:
                    pts.extend([target_x, self.cy - abs(r * 0.75 * round_dome) * dy])
                elif mode == "bottom" and is_behind:
                    pts.extend([target_x, self.cy + abs(r * 0.75 * round_dome) * dy])
                elif mode == "front" and not is_behind:
                    pts.extend([target_x, self.cy + abs(r * 0.25 * round_dome) * dy])
            if len(pts) >= 4: self.canvas.coords(ring["id"], *pts)

# ==========================================
# ЧАСТЬ 3: Реалистичная вспышка звезды и основной цикл
# ==========================================
    def trigger_star_flare(self):
        for item in self.flare_elements:
            self.canvas.delete(item)
        self.flare_elements.clear()

        self.flare_frame += 1
        max_flare_frames = 12  
        
        if self.flare_frame <= max_flare_frames:
            intensity = (max_flare_frames - self.flare_frame) / max_flare_frames
            
            # Фотометрическое ядро (наслоение мягких дисков свечения)
            steps = 5
            for s in range(steps):
                r_core = (50 * self.scale * intensity) * ((s + 1) / steps)
                c_val = int(210 + 45 * (s / steps))
                glow_color = f"#{c_val:02x}{int(c_val*0.95):02x}{int(c_val*0.95):02x}" if s > 2 else "#FFFFFF"
                core_id = self.canvas.create_oval(self.cx - r_core, self.cy - r_core, self.cx + r_core, self.cy + r_core, fill=glow_color, outline="")
                self.flare_elements.append(core_id)

            # Формирование дифракционных лучей звезды (плавные вытянутые конусы)
            ray_length = 240 * self.scale * math.pow(intensity, 1.4)
            ray_thickness = 7 * self.scale * intensity
            ray_color = f"#{int(220*intensity):02x}{int(235*intensity):02x}ff"
            
            h_ray = self.canvas.create_polygon(
                self.cx - ray_length, self.cy,
                self.cx, self.cy - ray_thickness,
                self.cx + ray_length, self.cy,
                self.cx, self.cy + ray_thickness,
                fill=ray_color, outline=""
            )
            v_ray = self.canvas.create_polygon(
                self.cx, self.cy - ray_length,
                self.cx - ray_thickness, self.cy,
                self.cx, self.cy + ray_length,
                self.cx + ray_thickness, self.cy,
                fill=ray_color, outline=""
            )
            self.flare_elements.extend([h_ray, v_ray])
            
            # Поднимаем вспышку на передний план над всеми элементами
            for item in self.flare_elements:
                self.canvas.tag_raise(item)
                
            self.root.after(55, self.trigger_star_flare)

    def animate(self):
        self.frame += 1
        dt = 2.2  
        virtual_frame = self.frame * dt
        
        start_frame = 10        
        transform_duration = 18 
        
        progress = 0.0 if self.frame <= start_frame else min(1.0, (self.frame - start_frame) / transform_duration)
        
        for star in self.topo.sky_stars:
            if progress >= 0.3: self.canvas.itemconfigure(star["id"], state="hidden")
            else: self.canvas.itemconfigure(star["id"], fill="#00FF00" if ((math.sin(virtual_frame * star["blink_speed"] + star["blink_phase"]) + 1) / 2) < 0.08 else star["base_color"])
        
        # ТОЧНЫЙ ТАЙМИНГ: Черная дыра активна строго в диапазоне 0.10 < progress < 0.75
        in_black_hole = (0.10 < progress < 0.75)
        
        for b in self.topo.galaxy_branches:
            for i in range(39):
                x1, y1 = self.topo.sample_spiral_path(i / 40, b, progress, virtual_frame, self.logo_r, self.bar_offset)
                x2, y2 = self.topo.sample_spiral_path((i + 1) / 40, b, progress, virtual_frame, self.logo_r, self.bar_offset)
                self.canvas.coords(b["segments"][i], x1, y1, x2, y2)
                orig_w = max(2.5 * self.scale, (6.0 * self.scale if b["is_milk"] else 4.5 * self.scale) * (1.0 - (i / 40) * (0.5 if b["is_milk"] else 0.7)))
                target_w = (44 * self.scale) if (b["phase"] < math.pi / 2 or (math.pi <= b["phase"] < 3 * math.pi / 2)) else (12 * self.scale)
                self.canvas.itemconfigure(b["segments"][i], width=orig_w + (target_w - orig_w) * progress)
                if progress > 0.0: self.canvas.itemconfigure(b["segments"][i], fill="#F0F8FF")
                
        for star in self.topo.galaxy_stars:
            if in_black_hole and star["t"] < 0.22:
                self.canvas.coords(star["id"], -10, -10, -10, -10)
                continue
            sx, sy = self.topo.sample_spiral_path(star["t"], star["branch"], progress, virtual_frame, self.logo_r, self.bar_offset)
            if progress > 0.2: self.canvas.itemconfigure(star["id"], fill="#F0F8FF")
            self.canvas.coords(star["id"], sx, sy, sx + star["size"], sy + star["size"])
        
        cos_a, sin_a = math.cos(virtual_frame * 0.12), math.sin(virtual_frame * 0.12)
        for pt in self.topo.core_particles:
            if progress == 0.0:
                bx, by = self.cx + (pt["local_x"] * cos_a - pt["local_y"] * sin_a), self.cy + (pt["local_x"] * sin_a + pt["local_y"] * cos_a)
            else:
                if in_black_hole and pt["t_factor"] < 0.22:
                    self.canvas.coords(pt["id"], -10, -10, -10, -10)
                    continue
                bx, by = self.topo.sample_spiral_path(pt["t_factor"], pt["branch"], progress, virtual_frame, self.logo_r, self.bar_offset)
                bx = bx + (pt["local_x"] * cos_a - pt["local_y"] * sin_a) * (1.0 - progress)
                by = by + (pt["local_x"] * sin_a + pt["local_y"] * cos_a) * (1.0 - progress)
                self.canvas.itemconfigure(pt["id"], fill="#F0F8FF")
            self.canvas.coords(pt["id"], bx, by, bx + 2, by + 2)
        
        if in_black_hole:
            wave = math.pow(math.sin(((progress - 0.10) / 0.65) * math.pi), 0.5) * (1.0 + 0.15 * progress)
            dy = 1.0 + 0.15 * math.sin(virtual_frame * 0.3)
            
            self.draw_lensed_rings(self.topo.back_rings, wave, dy, "back")
            self.draw_lensed_rings(self.topo.bottom_rings, wave, dy, "bottom")
            self.canvas.itemconfigure(self.shadow_id, state="normal")
            sh_size = 66 * self.scale * (wave / (1.0 + 0.15 * progress))
            self.canvas.coords(self.shadow_id, self.cx - sh_size, self.cy - sh_size, self.cx + sh_size, self.cy + sh_size)
            self.canvas.tag_raise(self.shadow_id)
            self.draw_lensed_rings(self.topo.front_rings, wave, dy, "front")
            for ring in self.topo.front_rings:
                self.canvas.tag_raise(ring["id"])
        else:
            # МГНОВЕННЫЙ СХЛОП: Как только progress преодолевает 0.75, черная дыра удаляется,
            # и звезда вспыхивает РОВНО в этот же кадр, закрывая собой ядро.
            self.canvas.itemconfigure(self.shadow_id, state="hidden")
            for r in self.topo.back_rings + self.topo.front_rings + self.topo.bottom_rings: 
                self.canvas.itemconfigure(r["id"], state="hidden")
            
            if progress >= 0.75 and not self.flare_triggered:
                self.flare_triggered = True
                self.canvas.delete(self.shadow_id)
                self.trigger_star_flare()
            
        if progress == 1.0:
            for el in [self.logo_circle, self.logo_bar1, self.logo_bar2]: self.canvas.itemconfigure(el, state="normal")
            self.canvas.coords(self.logo_circle, self.cx - self.logo_r, self.cy - self.logo_r, self.cx + self.logo_r, self.cy + self.logo_r)
            self.canvas.coords(self.logo_bar1, self.cx - 100 * self.scale, self.cy - self.bar_offset, self.cx + 100 * self.scale, self.cy - self.bar_offset)
            self.canvas.coords(self.logo_bar2, self.cx - 100 * self.scale, self.cy + self.bar_offset, self.cx + 100 * self.scale, self.cy + self.bar_offset)
            for b in self.topo.galaxy_branches:
                for s in b["segments"]: self.canvas.itemconfigure(s, state="hidden")
            for s in self.topo.galaxy_stars: self.canvas.itemconfigure(s["id"], state="hidden")
            for pt in self.topo.core_particles: self.canvas.itemconfigure(pt["id"], state="hidden")
            
            # Ожидание перед закрытием перенесено в окончание анимации вспышки
            self.root.after(600, lambda: self.blink_logo(step=0))
            return

        if progress < 1.0: self.root.after(180, self.animate)

    def blink_logo(self, step):
        logo_elements = [self.logo_circle, self.logo_bar1, self.logo_bar2]
        if step == 0:
            self.root.after(0, lambda: self.blink_logo(1))
        elif step == 1:
            for el in logo_elements: self.canvas.itemconfigure(el, state="hidden")
            self.root.after(50, lambda: self.blink_logo(2))
        elif step == 2:
            for el in logo_elements: self.canvas.itemconfigure(el, state="normal")
            self.root.after(350, self.root.destroy)

root = Tk()
app = ElegantGalacticTransform(root)
root.mainloop()
