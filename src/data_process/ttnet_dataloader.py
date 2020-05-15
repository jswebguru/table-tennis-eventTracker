from torch.utils.data import DataLoader

from data_process.ttnet_dataset import TTNet_Dataset
from data_process.ttnet_data_utils import get_events_infor, train_val_data_separation
from data_process.transformation import Compose, Random_Crop, Resize, Normalize, Random_Rotate, Random_HFlip


def create_train_val_dataloader(configs):
    """
    Create dataloader for training and validate
    Args:
        configs:

    Returns:

    """
    train_transform = Compose([
        Random_Crop(max_height_reduction_percent=0.15, max_width_reduction_percent=0.15, p=1.),
        Resize(new_size=(320, 128), p=1.0),
        Random_HFlip(p=0.5),
        Random_Rotate(rotation_angle_limit=15, p=0.5),
        Normalize(p=1.)
    ], p=1.)

    val_transform = Compose([
        Random_Crop(max_height_reduction_percent=0.15, max_width_reduction_percent=0.15, p=1.),
        Resize(new_size=(320, 128), p=1.0),
        Normalize(p=1.)
    ], p=1.)

    train_events_infor, val_events_infor = train_val_data_separation(configs)

    train_dataset = TTNet_Dataset(train_events_infor, configs.events_dict, transformations=train_transform)

    val_dataset = TTNet_Dataset(val_events_infor, configs.events_dict, transformations=val_transform)

    train_dataloader = DataLoader(train_dataset, batch_size=configs.batch_size, shuffle=True,
                                  pin_memory=configs.pin_memory, num_workers=configs.num_workers)

    val_dataloader = DataLoader(val_dataset, batch_size=configs.batch_size, pin_memory=configs.pin_memory,
                                num_workers=configs.num_workers)
    return train_dataloader, val_dataloader


def create_test_dataloader(configs):
    """
    Create dataloader for testing phase
    Args:
        configs:

    Returns:

    """
    test_transform = Compose([
        Random_Crop(max_height_reduction_percent=0.15, max_width_reduction_percent=0.15, p=1.),
        Resize(new_size=(320, 128), p=1.0),
        Normalize(p=1.)
    ], p=1.)
    dataset_type = 'test'
    test_events_infor = get_events_infor(configs.train_game_list, configs, dataset_type)
    test_dataset = TTNet_Dataset(test_events_infor, configs.events_dict, transformations=test_transform)

    test_dataloader = DataLoader(test_dataset, batch_size=configs.batch_size, pin_memory=configs.pin_memory,
                                 num_workers=configs.num_workers)
    return test_dataloader


if __name__ == '__main__':
    from config.config import parse_configs

    configs = parse_configs()
    train_dataloader, val_dataloader = create_train_val_dataloader(configs)
    for b_idx, (file_paths, points_sets, targets) in enumerate(train_dataloader):
        if b_idx != 0:
            break
        print('points_sets: {}, targets: {}'.format(points_sets.size(), targets.size()))
