import torch.nn as nn
import torch


class Ball_Detection_Loss(nn.Module):
    def __init__(self, w, h, epsilon=1e-9):
        super(Ball_Detection_Loss, self).__init__()
        self.w = w
        self.h = h
        self.epsilon = epsilon

    def forward(self, pred_ball_position, target_ball_position):
        x_pred = pred_ball_position[:, :self.w]
        y_pred = pred_ball_position[:, self.w: (self.w + self.h)]

        x_target = target_ball_position[:, :self.w]
        y_target = target_ball_position[:, self.w: (self.w + self.h)]

        loss_ball_x = - torch.mean(
            x_target * torch.log(x_pred + self.epsilon) + (1 - x_target) * torch.log(1 - x_pred + self.epsilon), dim=-1)
        loss_ball_y = - torch.mean(
            y_target * torch.log(y_pred + self.epsilon) + (1 - y_target) * torch.log(1 - y_pred + self.epsilon), dim=-1)
        return loss_ball_x + loss_ball_y


class Events_Spotting_Loss(nn.Module):
    def __init__(self, weights=(1, 3), num_events=2, epsilon=1e-9):
        super(Events_Spotting_Loss, self).__init__()
        self.weights = torch.tensor(weights).view(1, 2)
        self.num_events = num_events
        self.epsilon = epsilon

    def forward(self, pred_events, target_events):
        self.weights = self.weights.cuda()
        loss_event = - torch.mean(self.weights * (
                    target_events * torch.log(pred_events + self.epsilon) + (1. - target_events) * torch.log(
                1 - pred_events + self.epsilon)), dim=-1)

        return loss_event


class DICE_Smotth_Loss(nn.Module):
    def __init__(self, epsilon=1e-9):
        super(DICE_Smotth_Loss, self).__init__()
        self.epsilon = epsilon

    def forward(self, pred_seg, target_seg):
        union = pred_seg * target_seg
        loss_dice_smooth = (torch.sum(2 * union, dim=(1, 2, 3)) + self.epsilon) / (
                torch.sum(pred_seg, dim=(1, 2, 3)) + torch.sum(target_seg, dim=(1, 2, 3)) + self.epsilon)

        return loss_dice_smooth


class BCE_Loss(nn.Module):
    def __init__(self, epsilon=1e-9):
        super(BCE_Loss, self).__init__()
        self.epsilon = epsilon

    def forward(self, pred_seg, target_seg):
        bce_loss = - torch.mean(
            target_seg * torch.log(pred_seg + self.epsilon) + (1 - target_seg) * torch.log(1 - pred_seg + self.epsilon),
            dim=(1, 2, 3))

        return bce_loss


class Segmentation_Loss(nn.Module):
    def __init__(self):
        super(Segmentation_Loss, self).__init__()
        self.bce_criterion = BCE_Loss(epsilon=1e-9)
        self.dice_criterion = DICE_Smotth_Loss(epsilon=1e-9)

    def forward(self, pred_seg, target_seg):
        target_seg = target_seg.float()
        loss_bce = self.bce_criterion(pred_seg, target_seg.float())
        loss_dice = self.dice_criterion(pred_seg, target_seg)
        loss_seg = (1. - loss_dice) + loss_bce

        return loss_seg
