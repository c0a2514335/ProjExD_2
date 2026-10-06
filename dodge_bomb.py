import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内にあるか判定する関数
    引数：こうかとんRect または 爆弾Rect
    戻り値：タプル(横方向判定, 縦方向判定)
            画面内なら True / 画面外なら False
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数：screen Surface
    ブラックアウト表示、泣いているこうかとん、Game Overテキストを描画し5秒間停止する
    """
    black_img = pg.Surface((WIDTH, HEIGHT))
    black_img.fill((0, 0, 0))
    black_img.set_alpha(180)

    font = pg.font.Font(None, 80)
    txt_surface = font.render("Game Over", True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    cry_img = pg.image.load("fig/8.png")
    cry_rect_left = cry_img.get_rect(center=(txt_rect.left - 50, HEIGHT // 2))
    cry_rect_right = cry_img.get_rect(center=(txt_rect.right + 50, HEIGHT // 2))

    black_img.blit(txt_surface, txt_rect)
    black_img.blit(cry_img, cry_rect_left)
    black_img.blit(cry_img, cry_rect_right)

    screen.blit(black_img, [0, 0])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズが異なる爆弾Surfaceのリストと加速度のリストを生成する関数（追加機能2）
    戻り値：(爆弾Surfaceのリスト, 加速度のリスト)
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾Surfaceと加速度リストの初期化
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if not check_bound(kk_rct)[0] or not check_bound(kk_rct)[1]:
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾の拡大・加速および移動処理（追加機能2）
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()