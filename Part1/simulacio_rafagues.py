import argparse
import numpy as np
import pandas as pd


def fogm_process(delta_x, delta_y, dt_tau, w_x_0, w_y_0):

    fogm_x = np.exp(-dt_tau) * w_x_0 + delta_x * np.random.normal(0, 1)
    fogm_y = np.exp(-dt_tau) * w_y_0 + delta_y * np.random.normal(0, 1)

    return fogm_x, fogm_y


def delta(dt_tau, sigma_x, sigma_y):

    delta_x = sigma_x * np.sqrt(1 - np.exp(-2*dt_tau))
    delta_y = sigma_y * np.sqrt(1 - np.exp(-2*dt_tau))

    return delta_x, delta_y


def sigma(wind_df):  # standard deviation
    
    dir_rad = np.radians(wind_df['dir'])
    vel_x = wind_df['vel'] * np.cos(dir_rad)
    vel_y = wind_df['vel'] * np.sin(dir_rad)

    return np.std(vel_x), np.std(vel_y)


def replace_wind_values(wind_df, dt_tau, wx0, wy0):

    num_rows = wind_df.shape[0]

    sigma_x, sigma_y = sigma(wind_df)
    delta_x, delta_y = delta(dt_tau, sigma_x, sigma_y)

    vel_vect = []
    dir_vect = []

    for _ in range(num_rows):
        
        w_x, w_y = fogm_process(delta_x, delta_y, dt_tau, wx0, wy0)
        w = np.sqrt(w_x**2 + w_y**2)
        dir = (np.degrees(np.arctan2(w_y, w_x))) % 360

        vel_vect.append(w)
        dir_vect.append(dir)

        wx0 = w_x
        wy0 = w_y
    
    wind_df['vel'] = np.round(vel_vect).astype(int)
    wind_df['dir'] = np.round(dir_vect).astype(int)
    
    return wind_df


def add_wind_values(wind_df, dt_tau):

    num_rows = wind_df.shape[0]

    sigma_x, sigma_y = sigma(wind_df)
    delta_x, delta_y = delta(dt_tau, sigma_x, sigma_y)

    ts_inside = 3

    new_wind_df = wind_df.copy()

    for n_row in range(num_rows):

        wx0 = wind_df["vel"].iloc[n_row] * np.cos(np.radians(wind_df["dir"].iloc[n_row]))
        wy0 = wind_df["vel"].iloc[n_row] * np.sin(np.radians(wind_df["dir"].iloc[n_row]))

        time_aux = 15

        up_wind_df = new_wind_df.iloc[:(1 + ts_inside) * n_row+1]
        down_wind_df = new_wind_df.iloc[(1 + ts_inside) * n_row+1:]

        for _ in range(ts_inside):

            w_x, w_y = fogm_process(delta_x, delta_y, dt_tau, wx0, wy0)
            w = np.sqrt(w_x**2 + w_y**2)
            dir = (np.degrees(np.arctan2(w_y, w_x))) % 360

            wx0 = w_x
            wy0 = w_y

            time = up_wind_df["hora"].iloc[len(up_wind_df) - 1][:-2] + str(time_aux)
            up_wind_df.loc[len(up_wind_df)] = [up_wind_df["mes"].loc[len(up_wind_df)-1], up_wind_df["dia"].loc[len(up_wind_df)-1], time, w, dir, up_wind_df["cloud"].loc[len(up_wind_df)-1]]
            time_aux += 15

            new_wind_df = pd.concat([up_wind_df, down_wind_df], ignore_index=True)
        
        new_wind_df['vel'] = new_wind_df['vel'].round(0)
        new_wind_df['dir'] = new_wind_df['dir'].round(0)

    return new_wind_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--wind_file_path', type=str, help='Path to the wind file', default='PontVIladoma/Input/GIS_themes/PontViladomar_wind.wnd')
    parser.add_argument('--tau', type=float, help='Time constant', default=10000)
    parser.add_argument('--vel', type=float, help='Wind initial velocity', default=3)
    parser.add_argument('--dir', type=float, help='Wind initial direction', default=15)
    parser.add_argument('--mode', type=str, help='replace/add', default='add')
    parser.add_argument('--output_file_path', type=str, help='Path to the output wind file', default='PontVIladoma/Input/GIS_themes/output.wnd')
    args = parser.parse_args()

    vel = args.vel
    dir = args.dir
    wx0 = vel * np.cos(np.radians(dir))
    wy0 = vel * np.sin(np.radians(dir))
    
    # Read the wind file
    wind_df = pd.read_csv(args.wind_file_path, sep=' ', header=None, dtype={0: str, 1: str, 2: str})
    wind_df.columns = ['mes', 'dia', 'hora', 'vel', 'dir', 'cloud']
    num_rows = wind_df.shape[0]

    if args.mode == 'replace':
        dt_tau = 1 / args.tau
        wind_df = replace_wind_values(wind_df, dt_tau, wx0, wy0)

    elif args.mode == 'add':
        dt_tau = 0.25 / args.tau
        wind_df = add_wind_values(wind_df, dt_tau)

    else:
        print('Invalid mode. Please choose between replace and add.')
        exit(1)

    wind_df.to_csv(args.output_file_path, sep=' ', index=False, header=False)