import pygame


def render_stack(surf, images, pos, rotation, spreadx=0, spready=1):
    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(
            rotated_img,
            (
                pos[0] - rotated_img.get_width() // 2 - i * spreadx,
                pos[1] - rotated_img.get_height() // 2 - i * spready,
            ),
        )
