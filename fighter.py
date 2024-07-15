import pygame.key


class Fighter():
    def __init__(self,player,x,y,surface,flip,sheet,animation_steps,data):
        self.size = data[0]
        self.scale = data[1]
        self.offset = data[2]
        self.update_time = pygame.time.get_ticks()
        self.gravity = 0
        self.animation_list = self.load_image(sheet,animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x,y,80,180))
        self.surface = surface
        self.health =10
        self.flip = flip
        self.running = False
        self.attacking = False
        self.jumping = False
        self.attack_cooldown = 0
        self.player = player
        self.attack_type = 0
        self.death = False
        self.hited = False

    def attack(self,target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_rect = pygame.Rect(self.rect.centerx - 2*self.rect.width*self.flip, self.rect.centery, 2*self.rect.width, self.rect.height)
            pygame.draw.rect(self.surface,(255,0,0),attack_rect)
            if attack_rect.colliderect(target.rect):
                target.health -= 10
                target.hited = True
                if target.health == 0:
                    target.death = True


    # if the new action is diff from the old one, change the self.action and reset the frame_index to zero to avoid the case that the
    # index will be out of range of the new_action's length
    def compare_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def update_frame(self):#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        timer = 50
        # difference actions will
        if self.death == True:
            self.compare_action(6)
        elif self.hited == True:
            self.compare_action(5)
        elif self.attacking:
            if self.attack_type == 1:
                self.compare_action(3)
            if self.attack_type == 2:
                self.compare_action(4)

        elif self.jumping:
            self.compare_action(2)
        elif self.running:
            self.compare_action(1)
        else:
            self.compare_action(0)
        self.image = self.animation_list[self.action][self.frame_index]

        #increase the frame_index to see that the charactaer is moving
        if pygame.time.get_ticks() - self.update_time >= timer:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
        # reset the index when it go into the end of the current action list

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.death  == True:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index =0
                if self.attacking ==True :
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5 :
                    self.hited = False
                    self.attacking = False
                    self.attack_cooldown = 20


    #extract image from sheet
    def load_image(self,sheet,animation_steps):
        animation_list =[]
        for y,animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sheet.subsurface(x * self.size, y * self.size,self.size,self.size)
                scaled_image = pygame.transform.scale_by(temp_img, self.scale)
                temp_img_list.append(scaled_image)
            animation_list.append(temp_img_list)
        return animation_list



    def player_input(self,target):
        self.running = False

        SPEED = 10
        dx =0
        dy =0
        keys = pygame.key.get_pressed()
        if self.death == False:
            if self.attacking == False:
                if self.player == 1:

                    if keys[pygame.K_d]:
                        self.running = True
                        dx = SPEED

                    if keys[pygame.K_a]:
                        self.running = True
                        dx = -SPEED
                    if self.jumping == False:
                        if keys[pygame.K_SPACE]:
                            self.jumping = True
                            dy = -15
                            self.gravity = dy

                    if keys[pygame.K_j] :
                        self.attack(target)
                        self.attack_type = 1
                    if keys[pygame.K_k]:
                        self.attack(target)
                        self.attack_type = 2
                elif self.player == 2:
                    if keys[pygame.K_RIGHT]:
                        self.running = True
                        dx = SPEED

                    if keys[pygame.K_LEFT]:
                        self.running = True
                        dx = -SPEED

                    if keys[pygame.K_o]:
                        self.attack(target)
                        self.attack_type = 1
                    if keys[pygame.K_p]:
                        self.attack(target)
                        self.attack_type = 2
                    if self.jumping == False:
                        if keys[pygame.K_UP]:
                            self.jumping = True
                            dy = -15
                            self.gravity = dy

        # ensure players face each other
        if target.rect.centerx < self.rect.centerx:
            self.flip = True
        else:
            self.flip = False

        #attack cooldown
        if self.attack_cooldown >0:
            self.attack_cooldown -= 1

        #
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > 1000:
            dx = 1000 - self.rect.right

        self.rect.x += dx
        self.rect.y += dy


    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >= 200:
            self.rect.bottom = 200
            self.jumping = False
    # def jump(self):
    #     self.jumping = True
    #     self.gravity = -15
    #     self.rect.y += self.gravity

    def draw(self):
        img = pygame.transform.flip(self.image,self.flip,False)
        self.surface.blit(img,(self.rect.x - self.offset[0],self.rect.y -self.offset[1]))



    def update(self,target):
        self.player_input(target)
        self.apply_gravity()
        self.update_frame()
