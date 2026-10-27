#!/usr/bin/env python3
"""
1024×600 window at 60 fps

api
pfd = PrimaryFlightDisplay()
pfd.set(airspeed_kts=130, altitude_ft=5000, ...)
pfd.run()                       # dummy

from pfd import PrimaryFlightDisplay, PFDConfig
cfg = PFDConfig(spd_width=130, horizon_size=280, ...)
pfd = PrimaryFlightDisplay(config=cfg)

standalone
python3 pfd.py
python3 pfd.py --fullscreen
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

import pygame

Color = Union[str, Tuple[int, int, int]]


def _c(val: Color) -> Tuple[int, int, int]:
    if isinstance(val, str):
        h = val.lstrip('#')
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return val


@dataclass
class FlightData:
    airspeed_kts: float = 0.0
    mach: float = 0.0
    altitude_ft: float = 0.0
    altitude_ref_hpa: float = 1013.25
    vsi_fpm: float = 0.0
    pitch_deg: float = 0.0
    roll_deg: float = 0.0
    heading_deg: float = 0.0
    track_deg: float = 0.0
    ground_speed_kts: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    alpha_deg: float = 0.0
    slip_skid: float = 0.0
    flight_dir_pitch: float = 0.0
    flight_dir_roll: float = 0.0
    fd_active: bool = False
    on_ground: bool = True


@dataclass
class PFDConfig:
    width: int = 1024
    height: int = 600
    fps: int = 60
    col_bg: Color = "#000000"

    outer_margin: int = 32

    # airspeed strip
    spd_width: int = 160
    spd_height: int = 520
    spd_margin_inner: int = 0
    spd_major_step: int = 10
    spd_minor_step: int = 5
    spd_unit_per_px: float = 0.2
    spd_label_font: int = 24
    spd_readout_font: int = 36
    spd_readout_h: int = 40
    spd_readout_w: int = 70
    spd_readout_off_x: int = -40
    spd_readout_off_y: int = 0
    spd_readout_bg: Color = "#000000"
    spd_readout_border: Color = "#d596e8"
    spd_readout_text: Color = "#d596e8"
    spd_border_color: Color = "#404040"
    spd_border_w: int = 2
    spd_bg: Color = "#1E1E1E"
    spd_tick_color: Color = "#FFFFFF"
    spd_tick_minor_color: Color = "#646464"
    spd_tick_major_len: float = 0.5
    spd_tick_minor_len: float = 0.25
    spd_number_color: Color = "#FFFFFF"
    spd_tick_thick: int = 2

    # altitude strip
    alt_width: int = 160
    alt_height: int = 520
    alt_margin_inner: int = 0
    alt_major_step: int = 100
    alt_minor_step: int = 50
    alt_unit_per_px: float = 2.0
    alt_label_font: int = 24
    alt_readout_font: int = 36
    alt_readout_h: int = 40
    alt_readout_w: int = 70
    alt_readout_off_x: int = 40
    alt_readout_off_y: int = 0
    alt_readout_bg: Color = "#000000"
    alt_readout_border: Color = "#36c8cb"
    alt_readout_text: Color = "#36c8cb"
    alt_border_color: Color = "#404040"
    alt_border_w: int = 2
    alt_bg: Color = "#1E1E1E"
    alt_tick_color: Color = "#FFFFFF"
    alt_tick_minor_color: Color = "#646464"
    alt_tick_major_len: float = 0.5
    alt_tick_minor_len: float = 0.25
    alt_number_color: Color = "#FFFFFF"
    alt_tick_thick: int = 2

    # VSI strip
    vsi_width: int = 80
    vsi_height: int = 260
    vsi_major_step: int = 100
    vsi_minor_step: int = 50
    vsi_unit_per_px: float = 2.5
    vsi_label_font: int = 16
    vsi_readout_font: int = 20
    vsi_readout_h: int = 20
    vsi_readout_w: int = 35
    vsi_readout_off_x: int = 20
    vsi_readout_off_y: int = 0
    vsi_readout_bg: Color = "#000000"
    vsi_readout_border: Color = "#1dd830"
    vsi_readout_text: Color = "#1dd830"
    vsi_border_color: Color = "#404040"
    vsi_border_w: int = 2
    vsi_bg: Color = "#1E1E1E"
    vsi_tick_color: Color = "#FFFFFF"
    vsi_tick_minor_color: Color = "#646464"
    vsi_tick_major_len: float = 0.5
    vsi_tick_minor_len: float = 0.25
    vsi_number_color: Color = "#FFFFFF"
    vsi_max_val: int = 4000
    vsi_tick_thick: int = 1

    # attitude horizon
    horizon_size: int = 400
    col_sky: Color = "#679DB6"
    col_gnd: Color = "#85491A"
    col_horizon_line: Color = "#FFFFFF"
    col_horizon_border: Color = "#404040"
    horizon_border_w: int = 2

    # pitch ladder
    pitch_px_per_deg: int = 10
    pitch_major_step: int = 10
    pitch_minor_step: int = 5
    pitch_line_major_half: int = 55
    pitch_line_minor_half: int = 28
    pitch_label_font: int = 18
    pitch_line_color: Color = "#FFFFFF"
    pitch_label_color: Color = "#FFFFFF"
    pitch_zero_len_half: int = 55
    pitch_line_thick: int = 2

    # roll indicator
    roll_radius: int = 120
    roll_tick_len: int = 15
    roll_tick_thick: int = 2
    roll_arrow_size: int = 15
    roll_marks: list = field(default_factory=lambda: [0, 10, -10, 20, -20, 30, -30, 45, -45, 60, -60])
    roll_color: Color = "#FFFFFF"

    # heading ticks on horizon
    hdg_major_step: int = 10
    hdg_minor_step: int = 5
    hdg_tick_h_major: int = 10
    hdg_tick_h_minor: int = 5
    hdg_deg_per_px: float = 0.25
    hdg_label_font: int = 16
    hdg_tick_color: Color = "#FFFFFF"
    hdg_label_color: Color = "#FFFFFF"
    hdg_tick_thick: int = 2

    # aircraft reference
    ref_dot_size: int = 4
    ref_dot_color: Color = "#E6E600"
    ref_wing_length: int = 40
    ref_wing_thick: int = 4
    ref_wing_gap: int = 20
    ref_stem_length: int = 20
    ref_stem_thick: int = 4
    ref_wing_color: Color = "#E6E600"
    ref_stem_color: Color = "#E6E600"

    # horizontal slip
    slip_h_half_w: int = 100
    slip_h_y_off: int = 150
    slip_h_x_off: int = 0
    slip_h_ball_r: int = 10
    slip_h_track_thick: int = 2
    slip_h_ball_thick: int = 2
    slip_h_track_color: Color = "#FFFFFF"
    slip_h_ball_color: Color = "#FFFFFF"
    slip_h_show_val: bool = True
    slip_h_val_font: int = 16
    slip_h_val_color: Color = "#FFFFFF"
    slip_h_val_margin: int = 5

    # vertical slip
    slip_v_half_h: int = 100
    slip_v_x_off: int = 150
    slip_v_y_off: int = 0
    slip_v_ball_r: int = 10
    slip_v_track_thick: int = 2
    slip_v_ball_thick: int = 2
    slip_v_track_color: Color = "#FFFFFF"
    slip_v_ball_color: Color = "#FFFFFF"
    slip_v_show_val: bool = True
    slip_v_val_font: int = 16
    slip_v_val_color: Color = "#FFFFFF"
    slip_v_val_margin: int = 10

    # info grid
    info_rows: int = 3
    info_cols: int = 5
    info_texts: list = field(default_factory=lambda: [["MACH", "G/S", "LOC", "CAT3", "AP1+2"],
                                                      ["", "", "", "DUAL", "1 FD 2"],
                                                      ["", "", "", "", "A/THR"]])
    info_fg: list = field(default_factory=lambda: [["#1dd830", "#1dd830", "#1dd830", "#FFFFFF", "#FFFFFF"],
                                                   ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"],
                                                   ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]])
    info_bg: list = field(default_factory=lambda: [["#000000" for _ in range(5)] for _ in range(3)])
    info_font_size: int = 24
    info_border_color: Color = "#404040"
    info_border_w: int = 2
    info_row_h: int = 24
    info_cell_border_color: Color = "#404040"
    info_cell_border_w: int = 2

    # GPS
    gps_font: int = 24
    gps_color: Color = "#FFFFFF"

    # flight director
    fd_half_len: int = 60
    fd_color: Color = "#C800C8"
    fd_thick: int = 2

    # GND flag
    gnd_font: int = 24
    gnd_color: Color = "#E6A000"


class PrimaryFlightDisplay:

    def __init__(self, config: Optional[PFDConfig] = None, fullscreen: bool = False):
        self.cfg = config or PFDConfig()
        self.data = FlightData()
        self._fullscreen = fullscreen
        self._screen: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None
        self._fonts: dict = {}

    def _layout(self):
        c = self.cfg
        W, H = c.width, c.height
        m = c.outer_margin

        spd_top = (H - c.spd_height) // 2
        alt_top = (H - c.alt_height) // 2
        vsi_top = (H - c.vsi_height) // 2

        spd_x0 = m
        spd_x1 = spd_x0 + c.spd_width

        alt_x1 = W - m
        alt_x0 = alt_x1 - c.alt_width

        vsi_x1 = alt_x0
        vsi_x0 = vsi_x1 - c.vsi_width

        cx0 = spd_x1 + c.spd_margin_inner + m
        cx1 = alt_x0 - c.alt_margin_inner - m
        cx_mid = (cx0 + cx1) // 2

        # margin = (H - gh - hs) / 3   (if gh > 0 else H - hs) / 2)
        hs = c.horizon_size
        gh = c.info_rows * c.info_row_h

        if gh > 0:
            eq_margin = (H - gh - hs) / 3.0
        else:
            eq_margin = (H - hs) / 2.0

        h_top = int(eq_margin + gh + (eq_margin if gh > 0 else 0))
        h_bot = h_top + hs
        h_cx = cx_mid
        h_cy = h_top + hs // 2

        grid_top = int(eq_margin)
        grid_bot = grid_top + gh

        return dict(
            spd_x0=spd_x0, spd_x1=spd_x1, spd_top=spd_top,
            spd_bot=spd_top + c.spd_height,
            alt_x0=alt_x0, alt_x1=alt_x1, alt_top=alt_top,
            alt_bot=alt_top + c.alt_height,
            vsi_x0=vsi_x0, vsi_x1=vsi_x1, vsi_top=vsi_top,
            vsi_bot=vsi_top + c.vsi_height,
            cx0=cx0, cx1=cx1, cx_mid=cx_mid,
            h_left=cx_mid - hs // 2, h_top=h_top,
            h_right=cx_mid + hs // 2, h_bot=h_bot,
            h_cx=h_cx, h_cy=h_cy,
            grid_top=grid_top, grid_bot=grid_bot,
        )

    def set(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self.data, k):
                setattr(self.data, k, v)

    def get(self, key: str):
        return getattr(self.data, key, None)

    def init_window(self) -> None:
        c = self.cfg
        pygame.init()
        flags = pygame.FULLSCREEN if self._fullscreen else 0
        self._screen = pygame.display.set_mode((c.width, c.height), flags)
        pygame.display.set_caption("PFD")
        self._clock = pygame.time.Clock()
        self._fonts = dict(
            spd_lbl=pygame.font.Font(None, c.spd_label_font),
            spd_rout=pygame.font.Font(None, c.spd_readout_font),
            alt_lbl=pygame.font.Font(None, c.alt_label_font),
            alt_rout=pygame.font.Font(None, c.alt_readout_font),
            vsi_lbl=pygame.font.Font(None, c.vsi_label_font),
            vsi_rout=pygame.font.Font(None, c.vsi_readout_font),
            pitch_lbl=pygame.font.Font(None, c.pitch_label_font),
            hdg_lbl=pygame.font.Font(None, c.hdg_label_font),
            info=pygame.font.Font(None, c.info_font_size),
            gps=pygame.font.Font(None, c.gps_font),
            gnd=pygame.font.Font(None, c.gnd_font),
            slip_h_val=pygame.font.Font(None, c.slip_h_val_font),
            slip_v_val=pygame.font.Font(None, c.slip_v_val_font),
        )

    def close(self) -> None:
        pygame.quit()

    def run(self, dummy: bool = True) -> None:
        self.init_window()
        try:
            while True:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        return
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                        return
                if dummy:
                    self._inject_dummy()
                self.render()
                pygame.display.flip()
                self._clock.tick(self.cfg.fps)
        finally:
            self.close()

    _dummy_t: float = 0.0

    def _inject_dummy(self) -> None:
        t = self._dummy_t
        self._dummy_t += 1.0 / self.cfg.fps
        self.set(
            airspeed_kts=160 + 30 * math.sin(t * 0.5),
            altitude_ft=5000 + 200 * math.sin(t * 0.3),
            vsi_fpm=800 * math.sin(t * 0.3),
            pitch_deg=10 * math.sin(t * 0.7),
            roll_deg=25 * math.sin(t * 0.4),
            heading_deg=(t * 20) % 360,
            track_deg=(t * 20 + 2 * math.sin(t)) % 360,
            ground_speed_kts=155 + 25 * math.sin(t * 0.5),
            slip_skid=0.6 * math.sin(t * 0.9),
            alpha_deg=5 + 3 * math.sin(t * 0.6),
            mach=0.35 + 0.05 * math.sin(t * 0.5),
            latitude=47.0 + 0.01 * math.sin(t * 0.1),
            longitude=8.0 + 0.01 * math.cos(t * 0.1),
            on_ground=False,
        )

    def render(self) -> None:
        s = self._screen
        c = self.cfg
        L = self._layout()
        s.fill(_c(c.col_bg))
        self._draw_attitude(s, L)
        self._draw_heading_ticks(s, L)
        self._draw_airspeed_tape(s, L)
        self._draw_altitude_tape(s, L)
        self._draw_vsi_tape(s, L)
        self._draw_slip_h(s, L)
        self._draw_slip_v(s, L)
        self._draw_info_grid(s, L)
        self._draw_gps(s, L)
        self._draw_flight_director(s, L)
        self._draw_gnd(s, L)

    @staticmethod
    def _clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def _txt(self, font, text, color, pos, center=False):
        surf = font.render(str(text), True, _c(color))
        r = surf.get_rect()
        if center:
            r.center = (int(pos[0]), int(pos[1]))
        else:
            r.topleft = (int(pos[0]), int(pos[1]))
        self._screen.blit(surf, r)

    # attitude

    def _draw_attitude(self, s, L):
        c = self.cfg
        d = self.data
        cx, cy = L['h_cx'], L['h_cy']
        hs = c.horizon_size
        h_left, h_top = L['h_left'], L['h_top']
        h_right, h_bot = L['h_right'], L['h_bot']
        roll_rad = math.radians(d.roll_deg)

        pitch_px = d.pitch_deg * c.pitch_px_per_deg
        h_y = cy + pitch_px

        half_w = hs // 2 + 80
        cos_r, sin_r = math.cos(roll_rad), math.sin(roll_rad)
        dx = half_w * cos_r
        dy = half_w * sin_r
        hl = (cx - dx, h_y + dy)
        hr = (cx + dx, h_y - dy)

        sky_pts = [(h_left, h_top), (h_right, h_top), hr, hl]
        gnd_pts = [hl, hr, (h_right, h_bot), (h_left, h_bot)]
        pygame.draw.polygon(s, _c(c.col_sky), sky_pts)
        pygame.draw.polygon(s, _c(c.col_gnd), gnd_pts)
        pygame.draw.line(s, _c(c.col_horizon_line), hl, hr, 2)

        self._draw_pitch_ladder(s, L, cx, cy, roll_rad, pitch_px)
        self._draw_roll_indicator(s, L, cx, cy, roll_rad)
        self._draw_aircraft_ref(s, L, cx, cy)

        pygame.draw.rect(s, _c(c.col_bg), (0, 0, h_left, c.height))
        pygame.draw.rect(s, _c(c.col_bg), (h_right, 0, c.width - h_right, c.height))
        pygame.draw.rect(s, _c(c.col_bg), (h_left, 0, hs, h_top))
        pygame.draw.rect(s, _c(c.col_bg), (h_left, h_bot, hs, c.height - h_bot))

        pygame.draw.rect(s, _c(c.col_horizon_border), (h_left, h_top, hs, hs), c.horizon_border_w)

    # pitch ladder

    def _draw_pitch_ladder(self, s, L, cx, cy, roll_rad, pitch_px):
        c = self.cfg
        d = self.data
        pxd = c.pitch_px_per_deg
        cos_r, sin_r = math.cos(roll_rad), math.sin(roll_rad)

        def rot(px_, py_):
            dx_, dy_ = px_ - cx, py_ - cy
            return (cx + dx_ * cos_r + dy_ * sin_r, cy - dx_ * sin_r + dy_ * cos_r)

        for p in range(-90, 91, c.pitch_minor_step):
            # line_cy = h_y - p * pxd  =  cy + (pitch_deg - p) * pxd
            line_cy = cy + (d.pitch_deg - p) * pxd
            if p == 0:
                half = c.pitch_zero_len_half
            elif p % c.pitch_major_step == 0:
                half = c.pitch_line_major_half
            else:
                half = c.pitch_line_minor_half

            p0 = rot(cx - half, line_cy)
            p1 = rot(cx + half, line_cy)
            if p0[1] < -50 and p1[1] < -50:
                continue
            if p0[1] > c.height + 50 and p1[1] > c.height + 50:
                continue

            pygame.draw.line(s, _c(c.pitch_line_color), p0, p1, c.pitch_line_thick)

            if p != 0 and p % c.pitch_major_step == 0:
                label = f"{abs(p)}"
                r_pos = rot(cx + half + 5, line_cy)
                l_pos = rot(cx - half - 20, line_cy)
                self._txt(self._fonts['pitch_lbl'], label, c.pitch_label_color, r_pos)
                self._txt(self._fonts['pitch_lbl'], label, c.pitch_label_color, l_pos)

    # roll indicator

    def _draw_roll_indicator(self, s, L, cx, cy, roll_rad):
        c = self.cfg
        r = c.roll_radius
        top = -90
        for m in c.roll_marks:
            a = math.radians(top + m)
            inner = r - c.roll_tick_len
            x1 = cx + inner * math.cos(a)
            y1 = cy + inner * math.sin(a)
            x2 = cx + r * math.cos(a)
            y2 = cy + r * math.sin(a)
            pygame.draw.line(s, _c(c.roll_color), (x1, y1), (x2, y2), c.roll_tick_thick)
        a = math.radians(top + self.data.roll_deg)
        sz = c.roll_arrow_size
        px = cx + (r + 3) * math.cos(a)
        py = cy + (r + 3) * math.sin(a)
        perp = a + math.pi / 2
        pts = [
            (px + sz * math.cos(a), py + sz * math.sin(a)),
            (px + sz * 0.5 * math.cos(perp), py + sz * 0.5 * math.sin(perp)),
            (px - sz * 0.5 * math.cos(perp), py - sz * 0.5 * math.sin(perp)),
        ]
        pygame.draw.polygon(s, _c(c.roll_color), pts)

    # aircraft reference

    def _draw_aircraft_ref(self, s, L, cx, cy):
        c = self.cfg
        ds = c.ref_dot_size
        pygame.draw.rect(s, _c(c.ref_dot_color), (cx - ds, cy - ds, 2 * ds, 2 * ds))
        gap = c.ref_wing_gap + ds
        wl = c.ref_wing_length
        pygame.draw.line(s, _c(c.ref_wing_color), (cx - gap, cy), (cx - gap - wl, cy), c.ref_wing_thick)
        pygame.draw.line(s, _c(c.ref_wing_color), (cx + gap, cy), (cx + gap + wl, cy), c.ref_wing_thick)
        sl = c.ref_stem_length
        pygame.draw.line(s, _c(c.ref_stem_color), (cx - gap, cy), (cx - gap, cy + sl), c.ref_stem_thick)
        pygame.draw.line(s, _c(c.ref_stem_color), (cx + gap, cy), (cx + gap, cy + sl), c.ref_stem_thick)

    # heading ticks on horizon

    def _draw_heading_ticks(self, s, L):
        c = self.cfg
        d = self.data
        cx, cy = L['h_cx'], L['h_cy']
        hs = c.horizon_size
        roll_rad = math.radians(d.roll_deg)
        pitch_px = d.pitch_deg * c.pitch_px_per_deg
        h_y = cy + pitch_px   # horizon line y at centre (same as attitude draw)

        cos_r, sin_r = math.cos(roll_rad), math.sin(roll_rad)

        hdg = d.heading_deg % 360
        dpp = c.hdg_deg_per_px
        half_w = hs // 2
        vis_deg = int(half_w * dpp + 20)
        start = int(hdg - vis_deg) // c.hdg_minor_step * c.hdg_minor_step
        end = int(hdg + vis_deg) + c.hdg_minor_step

        CARD = {0: "N", 90: "E", 180: "S", 270: "W"}

        h_left, h_top = L['h_left'], L['h_top']
        s.set_clip(pygame.Rect(h_left, h_top, hs, hs))

        for deg in range(start, end, c.hdg_minor_step):
            deg_m = deg % 360
            dx = (deg - hdg) / dpp
            if abs(dx) > half_w + 20:
                continue
            major = (deg_m % c.hdg_major_step == 0)
            th = c.hdg_tick_h_major if major else c.hdg_tick_h_minor

            bx = cx + dx * cos_r
            by = h_y - dx * sin_r

            p_bot = (bx, by)
            p_top = (bx - th * sin_r, by - th * cos_r)

            pygame.draw.line(s, _c(c.hdg_tick_color), p_bot, p_top, c.hdg_tick_thick)

            if major:
                label = CARD.get(deg_m, f"{int(deg_m):03d}")
                lbl_off = th + 6
                lbl_pos = (bx - lbl_off * sin_r, by - lbl_off * cos_r)
                self._txt(self._fonts['hdg_lbl'], label, c.hdg_label_color, lbl_pos, center=True)

        s.set_clip(None)

    # generic tape

    def _draw_tape(self, s, L, *,
                   x0, width, top, bot,
                   value, major_step, minor_step, unit_per_px,
                   lbl_font_key, rout_font_key,
                   readout_h, readout_w, readout_off_x, readout_off_y,
                   readout_bg, readout_border, readout_text,
                   border_color, border_w, bg_color,
                   tick_color, tick_minor_color,
                   tick_major_len, tick_minor_len, number_color,
                   tick_thick,
                   ticks_on_right,
                   label_fmt=None,
                   ):
        c = self.cfg
        w = width
        h = bot - top
        cy = (top + bot) // 2

        pygame.draw.rect(s, _c(bg_color), (x0, top, w, h))

        s.set_clip(pygame.Rect(x0, top, w, h))

        vis_range = int(h * unit_per_px / 2 + major_step * 2)
        start_val = int((value - vis_range) // minor_step) * minor_step
        end_val = int((value + vis_range) // minor_step + 1) * minor_step

        for v in range(start_val, end_val, minor_step):
            dy = (value - v) / unit_per_px
            y = cy + dy
            if y < top + 1 or y > bot - 1:
                continue
            iy = int(y)
            major = (v % major_step == 0)
            frac = tick_major_len if major else tick_minor_len
            tick_len = int(w * frac)
            tc = tick_color if major else tick_minor_color

            if ticks_on_right:
                tx0 = x0 + w - tick_len - border_w
                tx1 = x0 + w - border_w
            else:
                tx0 = x0 + border_w
                tx1 = x0 + border_w + tick_len

            pygame.draw.line(s, _c(tc), (tx0, iy), (tx1, iy), tick_thick)

            if major:
                if label_fmt:
                    lbl = label_fmt(v)
                else:
                    lbl = str(v)
                if ticks_on_right:
                    num_cx = x0 + border_w + (w - tick_len - border_w * 2) // 2
                    self._txt(self._fonts[lbl_font_key], lbl, number_color,
                              (num_cx, iy), center=True)
                else:
                    num_cx = x0 + border_w + tick_len + (w - tick_len - border_w * 2) // 2
                    self._txt(self._fonts[lbl_font_key], lbl, number_color,
                              (num_cx, iy), center=True)

        rw = readout_w if readout_w > 0 else w
        rh = readout_h
        rx = x0 + (w - rw) // 2 + readout_off_x
        ry = cy - rh // 2 + readout_off_y
        rx = self._clamp(rx, x0, x0 + w - rw)
        ry = self._clamp(ry, top, bot - rh)
        pygame.draw.rect(s, _c(readout_bg), (rx, ry, rw, rh))
        pygame.draw.rect(s, _c(readout_border), (rx, ry, rw, rh), 2)
        val_str = f"{value:.0f}"
        self._txt(self._fonts[rout_font_key], val_str, readout_text,
                  (rx + rw // 2, ry + rh // 2), center=True)

        s.set_clip(None)

        pygame.draw.rect(s, _c(border_color), (x0, top, w, h), border_w)

    # airspeed tape

    def _draw_airspeed_tape(self, s, L):
        c = self.cfg
        self._draw_tape(s, L,
            x0=L['spd_x0'], width=c.spd_width, top=L['spd_top'], bot=L['spd_bot'],
            value=self.data.airspeed_kts,
            major_step=c.spd_major_step, minor_step=c.spd_minor_step,
            unit_per_px=c.spd_unit_per_px,
            lbl_font_key='spd_lbl', rout_font_key='spd_rout',
            readout_h=c.spd_readout_h, readout_w=c.spd_readout_w,
            readout_off_x=c.spd_readout_off_x, readout_off_y=c.spd_readout_off_y,
            readout_bg=c.spd_readout_bg, readout_border=c.spd_readout_border,
            readout_text=c.spd_readout_text,
            border_color=c.spd_border_color, border_w=c.spd_border_w,
            bg_color=c.spd_bg,
            tick_color=c.spd_tick_color, tick_minor_color=c.spd_tick_minor_color,
            tick_major_len=c.spd_tick_major_len, tick_minor_len=c.spd_tick_minor_len,
            number_color=c.spd_number_color,
            tick_thick=c.spd_tick_thick,
            ticks_on_right=True,
        )

    # altitude tape

    def _draw_altitude_tape(self, s, L):
        c = self.cfg
        self._draw_tape(s, L,
            x0=L['alt_x0'], width=c.alt_width, top=L['alt_top'], bot=L['alt_bot'],
            value=self.data.altitude_ft,
            major_step=c.alt_major_step, minor_step=c.alt_minor_step,
            unit_per_px=c.alt_unit_per_px,
            lbl_font_key='alt_lbl', rout_font_key='alt_rout',
            readout_h=c.alt_readout_h, readout_w=c.alt_readout_w,
            readout_off_x=c.alt_readout_off_x, readout_off_y=c.alt_readout_off_y,
            readout_bg=c.alt_readout_bg, readout_border=c.alt_readout_border,
            readout_text=c.alt_readout_text,
            border_color=c.alt_border_color, border_w=c.alt_border_w,
            bg_color=c.alt_bg,
            tick_color=c.alt_tick_color, tick_minor_color=c.alt_tick_minor_color,
            tick_major_len=c.alt_tick_major_len, tick_minor_len=c.alt_tick_minor_len,
            number_color=c.alt_number_color,
            tick_thick=c.alt_tick_thick,
            ticks_on_right=False,
            # label_fmt=lambda v: str(v // 100),
            # label_fmt=lambda v: f"{v:+.0f}",
        )

    # VSI tape

    def _draw_vsi_tape(self, s, L):
        c = self.cfg
        self._draw_tape(s, L,
            x0=L['vsi_x0'], width=c.vsi_width, top=L['vsi_top'], bot=L['vsi_bot'],
            value=self.data.vsi_fpm,
            major_step=c.vsi_major_step, minor_step=c.vsi_minor_step,
            unit_per_px=c.vsi_unit_per_px,
            lbl_font_key='vsi_lbl', rout_font_key='vsi_rout',
            readout_h=c.vsi_readout_h, readout_w=c.vsi_readout_w,
            readout_off_x=c.vsi_readout_off_x, readout_off_y=c.vsi_readout_off_y,
            readout_bg=c.vsi_readout_bg, readout_border=c.vsi_readout_border,
            readout_text=c.vsi_readout_text,
            border_color=c.vsi_border_color, border_w=c.vsi_border_w,
            bg_color=c.vsi_bg,
            tick_color=c.vsi_tick_color, tick_minor_color=c.vsi_tick_minor_color,
            tick_major_len=c.vsi_tick_major_len, tick_minor_len=c.vsi_tick_minor_len,
            number_color=c.vsi_number_color,
            tick_thick=c.vsi_tick_thick,
            ticks_on_right=False,
            label_fmt=lambda v: f"{v:+.0f}",
        )

    # horizontal slip

    def _draw_slip_h(self, s, L):
        c = self.cfg
        d = self.data
        cx = L['h_cx'] + c.slip_h_x_off
        y = L['h_cy'] + c.slip_h_y_off
        hw = c.slip_h_half_w
        pygame.draw.line(s, _c(c.slip_h_track_color), (cx - hw, y), (cx + hw, y), c.slip_h_track_thick)
        pygame.draw.line(s, _c(c.slip_h_track_color), (cx, y - 4), (cx, y + 4), c.slip_h_track_thick)
        bx = cx + int(d.slip_skid * hw)
        pygame.draw.circle(s, _c(c.slip_h_ball_color), (bx, y), c.slip_h_ball_r, c.slip_h_ball_thick)
        if c.slip_h_show_val:
            val_str = f"{d.slip_skid:+.2f}"
            self._txt(self._fonts['slip_h_val'], val_str, c.slip_h_val_color,
                      (cx + hw + c.slip_h_val_margin, y), center=False)

    # vertical slip

    def _draw_slip_v(self, s, L):
        c = self.cfg
        d = self.data
        x = L['h_cx'] - c.slip_v_x_off
        cy = L['h_cy'] + c.slip_v_y_off
        hh = c.slip_v_half_h
        pygame.draw.line(s, _c(c.slip_v_track_color), (x, cy - hh), (x, cy + hh), c.slip_v_track_thick)
        pygame.draw.line(s, _c(c.slip_v_track_color), (x - 4, cy), (x + 4, cy), c.slip_v_track_thick)
        by = cy - int(self._clamp(d.alpha_deg / 15.0, -1, 1) * hh)
        pygame.draw.circle(s, _c(c.slip_v_ball_color), (x, by), c.slip_v_ball_r, c.slip_v_ball_thick)
        if c.slip_v_show_val:
            val_str = f"{d.alpha_deg:.1f}"
            self._txt(self._fonts['slip_v_val'], val_str, c.slip_v_val_color,
                      (x, cy + hh + c.slip_v_val_margin), center=True)

    # info grid

    def _draw_info_grid(self, s, L):
        c = self.cfg
        gx0 = L['spd_x1'] + c.spd_margin_inner + c.outer_margin
        gx1 = L['alt_x0'] - c.alt_margin_inner - c.outer_margin
        gw = gx1 - gx0
        if gw <= 0:
            return
        rows, cols = c.info_rows, c.info_cols
        rh = c.info_row_h
        gh = rows * rh
        gy = L['grid_top']

        if gy < 0:
            return

        pygame.draw.rect(s, _c(c.info_border_color), (gx0, gy, gw, gh), c.info_border_w)

        cell_w = gw // cols
        for r in range(rows):
            for col in range(cols):
                cx_ = gx0 + col * cell_w
                cy_ = gy + r * rh
                cw_ = cell_w if col < cols - 1 else (gx0 + gw - cx_)
                ch_ = rh
                bg = c.info_bg[r][col] if r < len(c.info_bg) and col < len(c.info_bg[r]) else "#000000"
                fg = c.info_fg[r][col] if r < len(c.info_fg) and col < len(c.info_fg[r]) else "#FFFFFF"
                txt = c.info_texts[r][col] if r < len(c.info_texts) and col < len(c.info_texts[r]) else ""
                pygame.draw.rect(s, _c(bg), (cx_, cy_, cw_, ch_))
                pygame.draw.rect(s, _c(c.info_cell_border_color), (cx_, cy_, cw_, ch_), c.info_cell_border_w)
                if txt:
                    self._txt(self._fonts['info'], txt, fg,
                              (cx_ + cw_ // 2, cy_ + ch_ // 2), center=True)

    # GPS

    def _draw_gps(self, s, L):
        c = self.cfg
        d = self.data
        h_bot = L['h_bot']
        mid_y = (h_bot + c.height) // 2
        lat_s = f"{abs(d.latitude):.4f}{'N' if d.latitude >= 0 else 'S'}"
        lon_s = f"{abs(d.longitude):.4f}{'E' if d.longitude >= 0 else 'W'}"
        txt = f"{lat_s}  {lon_s}"
        self._txt(self._fonts['gps'], txt, c.gps_color, (L['cx_mid'], mid_y), center=True)

    # flight director

    def _draw_flight_director(self, s, L):
        c = self.cfg
        d = self.data
        if not d.fd_active:
            return
        cx, cy = L['h_cx'], L['h_cy']
        fd_y = cy - (d.flight_dir_pitch - d.pitch_deg) * c.pitch_px_per_deg
        hl = c.fd_half_len
        pygame.draw.line(s, _c(c.fd_color), (cx - hl, int(fd_y)), (cx + hl, int(fd_y)), c.fd_thick)
        fr = math.radians(d.flight_dir_roll)
        dx = hl * math.sin(fr)
        dy = hl * math.cos(fr)
        pygame.draw.line(s, _c(c.fd_color), (int(cx - dx), int(cy - dy)), (int(cx + dx), int(cy + dy)), c.fd_thick)

    # GND flag

    def _draw_gnd(self, s, L):
        if self.data.on_ground:
            c = self.cfg
            self._txt(self._fonts['gnd'], "GND", c.gnd_color,
                      (L['h_cx'], L['h_cy'] - 80), center=True)


def main():
    fullscreen = "--fullscreen" in sys.argv
    pfd = PrimaryFlightDisplay(fullscreen=fullscreen)
    c = pfd.cfg
    pfd.run(dummy=True)


if __name__ == "__main__":
    main()

