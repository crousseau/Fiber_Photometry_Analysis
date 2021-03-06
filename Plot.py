#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 13:19:37 2020

@author: thomas.topilko
"""

import os
import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.style.use("default")
import seaborn as sns
from sklearn.metrics import auc
import scipy.stats as stats

import Utilities as ut

def check_dF_with_behavior(position_bouts, length_bouts, color=["blue"], name="dF_&_behavioral_overlay", **kwargs):
    
    """Function that plots the pre-processed photometry data and overlays the
    behavior data.
    
    Args :  position_bouts (arr) = list of start and end of each behavioral bout
            length_bouts (list) = list of the length of each behavioral bout
            color (list) = color(s) of the behavioral overlay(s)
            kwargs (dict) = dictionnary with additional parameters
    """
    
    fig = plt.figure(figsize=(10,3), dpi=200.)
        
    ax0 = plt.subplot(111)
    
    n = 0
    handles = []
    
    if len(position_bouts) == 1 :
        labels = [kwargs["behavior_to_segment"]]
    else :
        labels = [kwargs["behavior_to_segment"], "Excluded"]
    
    ax0.plot(kwargs["photometry_data"]["dFF"]["x"], kwargs["photometry_data"]["dFF"]["dFF"], color="green", lw=kwargs["lw"])
    ax0.plot(0,  kwargs["video_end"]-kwargs["photometry_data"]["time_lost"], (0, 0), "--", color="blue", lw=kwargs["lw"]) #Creates a horizontal dashed line at y = 0 to signal the baseline
    
    xticks, xticklabels, unit = ut.generate_xticks_and_labels(kwargs["photometry_data"]["dFF"]["x"][-1])
    ax0.set_xticks(xticks)
    ax0.set_xticklabels(xticklabels, fontsize=kwargs["fsl"])
    ax0.set_xlim(0, kwargs["photometry_data"]["dFF"]["x"][-1])
    ax0.set_xlabel("Time ({0})".format(unit), fontsize=kwargs["fsl"])
    
    y_min, y_max, round_factor = ut.generate_yticks(kwargs["photometry_data"]["dFF"]["dFF"], 0.1)
    ax0.set_yticks(np.arange(y_min, y_max+round_factor, round_factor))
    ax0.set_ylim(y_min, y_max)
    
    if kwargs["photometry_pp"]["standardize"] :
        
        ax0.set_yticklabels(["{:.0f}".format(i) for i in np.arange(y_min, y_max+round_factor, round_factor)], fontsize=kwargs["fsl"])
        
    else :
        
        ax0.set_yticklabels(["{:.0f}".format(i) for i in np.arange(y_min, y_max+round_factor, round_factor)*100], fontsize=kwargs["fsl"])
        
    for P, L in zip(position_bouts, length_bouts) :
        
        patch = patches.Rectangle((0, 0), 1, 1, alpha=0.3, color=color[n], lw=0, edgecolor=None)
        handles.append(patch)
    
        for p, l in zip(P, L) :
            
            patch = patches.Rectangle((p[0], y_min+y_min*0.1), l, (y_max+y_max*0.1)-(y_min+y_min*0.1), alpha=0.3, color=color[n], lw=0, edgecolor=None)
            ax0.add_patch(patch)
            
        n += 1
        
    ax0.legend(handles=handles, labels=labels, loc=2, fontsize=kwargs["fsl"])
    plt.tight_layout()
    
    if kwargs["save"] :
        
        plt.savefig(os.path.join(kwargs["save_dir"], "{0}.{1}".format(name, kwargs["extension"])), dpi=200.)

def peri_event_plot(data_around_major_bouts, length_major_bouts, cmap="inferno", **kwargs) :
    
    """Function that plots the peri-event photometry data in two different formats.
    First a line plot showing the average signal before and after initiation of the behavior,
    Second a heatmap showing each individual signal traces before and after initiation of the behavior.
    
    Args :  data_around_major_bouts (arr) = list of the pre-processed photometry data
            before and after initiation of the behavior
            length_major_bouts (list) = list of the length of each behavioral bout
            cmap (str) = colormap used for the heatmap
            kwargs (dict) = dictionnary with additional parameters
    """
    
    mean_data_around_bouts = np.mean(data_around_major_bouts, axis=0) #Computes the mean for the peri-event photometry data
    std_data_around_bouts = np.std(data_around_major_bouts, axis=0) #Computes the standard deviation for the peri-event photometry data

    fig = plt.figure(figsize=(5, 5), dpi=200.) #Creates a figure
    
    # =============================================================================
    #     First Plot
    # =============================================================================
    
    ax0 = plt.subplot(2,1,1) #Creates a subplot for the first figure
    
    x_range = np.linspace(0, len(mean_data_around_bouts), len(mean_data_around_bouts))
    ax0.plot(x_range, mean_data_around_bouts, color="green", alpha=1., lw=kwargs["lw"]+1, zorder=1) #Plots the average signal
    
    if kwargs["peri_event"]["style"] == "individual" : #If individual traces are to be displayed in the line plot

        for l in data_around_major_bouts :
            
            if kwargs["peri_event"]["individual_color"] :
            
                ax0.plot(l, alpha=0.5, lw=kwargs["lw"], zorder=0) #Plots individual traces
                
            else :
                
                ax0.plot(l, color="gray", alpha=0.5, lw=kwargs["lw"], zorder=0) #Plots individual traces
            
        ax0.plot(x_range, mean_data_around_bouts + std_data_around_bouts, color="green", alpha=0.5, lw=kwargs["lw"], zorder=1)
        ax0.plot(x_range, mean_data_around_bouts - std_data_around_bouts, color="green", alpha=0.5, lw=kwargs["lw"], zorder=1)
        
        ax0.fill_between(x_range, mean_data_around_bouts, (mean_data_around_bouts + std_data_around_bouts),\
                         color="green", alpha=0.1)
        ax0.fill_between(x_range, mean_data_around_bouts, (mean_data_around_bouts - std_data_around_bouts),\
                         color="green", alpha=0.1)
        
        y_min, y_max, round_factor = ut.generate_yticks(data_around_major_bouts.flatten(), 0.2)
        y_range = y_max - y_min
        ax0.set_yticks(np.arange(y_min, y_max+round_factor, round_factor))
        ax0.set_yticklabels(["{:.0f}".format(i) for i in np.arange(y_min, y_max+round_factor, round_factor)], fontsize=kwargs["fsl"])
        ax0.set_ylim(y_min, y_max)
            
    elif kwargs["peri_event"]["style"] == "average" :
            
        ax0.plot(x_range, mean_data_around_bouts + std_data_around_bouts, color="green", alpha=0.3, lw=kwargs["lw"])
        ax0.plot(x_range, mean_data_around_bouts - std_data_around_bouts, color="green", alpha=0.3, lw=kwargs["lw"])
        
        ax0.fill_between(x_range, mean_data_around_bouts, (mean_data_around_bouts + std_data_around_bouts),\
                         color="green", alpha=0.1)
        ax0.fill_between(x_range, mean_data_around_bouts, (mean_data_around_bouts - std_data_around_bouts),\
                         color="green", alpha=0.1)
        
        y_min, y_max, round_factor = ut.generate_yticks(np.concatenate((mean_data_around_bouts + std_data_around_bouts, mean_data_around_bouts - std_data_around_bouts)), 0.2)
        y_range = y_max - y_min
        ax0.set_yticks(np.arange(y_min, y_max+round_factor, round_factor))
        ax0.set_yticklabels(["{:.0f}".format(i) for i in np.arange(y_min, y_max+round_factor, round_factor)], fontsize=kwargs["fsl"])
        ax0.set_ylim(y_min, y_max)
    
    #Creates a gray square on the line plot that represents the average length of a behavioral bout   
    patch = patches.Rectangle(((kwargs["peri_event"]["graph_distance_pre"]+0.5)*kwargs["recording_sampling_rate"], -y_range*0.1),\
                               width = np.mean(length_major_bouts)*kwargs["recording_sampling_rate"],\
                               height = y_range*0.1,\
                               color = "gray", 
                               lw = 0,
                               alpha = 0.7)
    
    ax0.add_patch(patch) #Adds the patch to the plot
    ax0.plot((0, len(mean_data_around_bouts)), (0, 0), "--", color="black", lw=kwargs["lw"]) #Creates a horizontal dashed line at y = 0 to signal the baseline
    vline = ax0.axvline(x=(kwargs["peri_event"]["graph_distance_pre"]+0.5)*kwargs["recording_sampling_rate"], color='red', linestyle='--', lw=kwargs["lw"]) #Creates a vertical dashed line at x = 0 to signal the begining of the behavioral bout
    
    ax0.set_xticks(np.linspace(0, ((kwargs["peri_event"]["graph_distance_pre"]+kwargs["peri_event"]["graph_distance_post"]+1)*kwargs["recording_sampling_rate"]), 5)) #Generates ticks for the x axis
    ax0.set_xticklabels(np.linspace(-kwargs["peri_event"]["graph_distance_pre"], kwargs["peri_event"]["graph_distance_post"], 5), fontsize=kwargs["fsl"]) #Generates labels for the x axis
    ax0.set_xlim(0, len(mean_data_around_bouts)) #Sets the limits for the x axis
#    ax0.set_xlabel("Time (s)", fontsize=kwargs["fsl"]) #Displays the label for the x axis

    ax0.legend(handles=[vline, patch], labels=["Begining of bout","Average behavioral bout length"], loc=2, fontsize=kwargs["fsl"]) #Displays the legend of the first figure
    
    # =============================================================================
    #     Second Plot
    # =============================================================================
    
    ax1 = plt.subplot(2,1,2) #Creates a subplot for the second figure
    
    if not kwargs["peri_event"]["normalize_heatmap"] :
        heatmap = ax1.imshow(data_around_major_bouts, cmap=cmap, aspect="auto", interpolation="none")
    else :
        heatmap = ax1.imshow(data_around_major_bouts, cmap=cmap, aspect="auto", norm=col.LogNorm(), interpolation="none") #norm=matplotlib.colors.LogNorm()
        
    ax1.axvline(x=(kwargs["peri_event"]["graph_distance_pre"]+0.5)*kwargs["recording_sampling_rate"], color='red', linestyle='--', lw=kwargs["lw"])
        
    ax1.set_xticks(np.linspace(0, ((kwargs["peri_event"]["graph_distance_pre"]+kwargs["peri_event"]["graph_distance_post"]+1)*kwargs["recording_sampling_rate"]), 5)) #Generates ticks for the x axis
    ax1.set_xticklabels(np.linspace(-kwargs["peri_event"]["graph_distance_pre"], kwargs["peri_event"]["graph_distance_post"], 5), fontsize=kwargs["fsl"]) #Generates labels for the x axis
    ax1.set_xlim(0, len(mean_data_around_bouts)) #Sets the limits for the x axis
    ax1.set_xlabel("Time (s)", fontsize=kwargs["fsl"]) #Displays the label for the x axis
    
    ax1.set_yticks([])
    ax1.set_ylim(-0.5, len(data_around_major_bouts)-0.5)
    ax1.set_ylabel("Duration of individual bouts (s)", fontsize=kwargs["fsl"], labelpad=20) #Displays the label for the x axis

    for n, l in enumerate(length_major_bouts) :
        
        ax1.text(-len(mean_data_around_bouts)*0.01, n, l, ha="right", va="center", fontsize=kwargs["fsl"])
    
    plt.gca().invert_yaxis()
    cax = fig.add_axes([1, 0.1, 0.02, 0.35])
    cb = plt.colorbar(heatmap, ax=ax1, cax=cax)
    cb.ax.tick_params(labelsize=kwargs["fsl"])
    cb.ax.get_yaxis().labelpad = 8
    
    if kwargs["photometry_pp"]["standardize"] :
        
        ax0.set_ylabel(r"$\Delta$F/F (Z-Score)", fontsize=kwargs["fsl"]) #Displays the label for the y axis
        ax0.set_title(r"$\Delta$F/F (Z-Score) in function of time before & after {0} initiation".format(kwargs["behavior_to_segment"]), fontsize=kwargs["fst"]) #Displays the titel for the first figure
        ax1.set_title(r"Individual $\Delta$F/F (Z-Score) in function of time before & after {0} initiation".format(kwargs["behavior_to_segment"]), fontsize=kwargs["fst"])
        cb.ax.set_ylabel(r"$\Delta$F/F (Z-Score)", rotation=270, fontsize=kwargs["fsl"])
        
    else :
        
        ax0.set_ylabel(r"$\Delta$F/F (%)", fontsize=kwargs["fsl"]) #Displays the label for the y axis
        ax0.set_title(r"$\Delta$F/F (%) in function of time before & after {0} initiation".format(kwargs["behavior_to_segment"]), fontsize=kwargs["fst"]) #Displays the titel for the first figure
        ax1.set_title(r"Individual $\Delta$F/F (%) in function of time before & after {0} initiation".format(kwargs["behavior_to_segment"]), fontsize=kwargs["fst"])
        cb.ax.set_ylabel(r"$\Delta$F/F (%)", rotation=270, fontsize=kwargs["fsl"])
        
    plt.tight_layout()
    
    if kwargs["save"] :
        
        plt.savefig(os.path.join(kwargs["save_dir"], "Peri_Event_Plot.{0}".format(kwargs["extension"])), dpi=200., bbox_inches='tight')
        
def peri_event_bar_plot(data_around_major_bouts, **kwargs) :
    
    """Function that compares the area under the curve (AUC) before and after the intitation of the behavior.
    The results are summarized in a bar plot showing the AUC before and after initiation of the behavior.
    
    Args :  data_around_major_bouts (arr) = list of the pre-processed photometry data
            kwargs (dict) = dictionnary with additional parameters
    """
    
    time_before = np.linspace(0, kwargs["peri_event"]["graph_auc_pre"], kwargs["peri_event"]["graph_auc_pre"]*kwargs["recording_sampling_rate"])
    data_before = data_around_major_bouts[:, 0 : kwargs["peri_event"]["graph_auc_pre"]*kwargs["recording_sampling_rate"]]
    
    time_after = np.linspace(0, kwargs["peri_event"]["graph_auc_post"], kwargs["peri_event"]["graph_auc_post"]*kwargs["recording_sampling_rate"])
    data_after = data_around_major_bouts[:, (kwargs["peri_event"]["graph_auc_pre"]+1)*kwargs["recording_sampling_rate"] : (kwargs["peri_event"]["graph_auc_pre"]+1+kwargs["peri_event"]["graph_auc_post"])*kwargs["recording_sampling_rate"]]
    
    all_AUC1 = [auc(time_before, i) for i in data_before]
    AUC1_mean = auc(time_before, np.mean(data_before, axis=0))
    AUC1_std = auc(time_before, np.std(data_before, axis=0))
    
    all_AUC2 = [auc(time_after, i) for i in data_after]
    AUC2_mean = auc(time_after, np.mean(data_after, axis=0))
    AUC2_std = auc(time_after, np.std(data_after, axis=0))

    AUC_mean = [AUC1_mean, AUC2_mean]
    AUC_std = [AUC1_std, AUC2_std]

    stat, pval = stats.ttest_ind(all_AUC1, all_AUC2, equal_var=False)
    
    fig = plt.figure(figsize=(5,5), dpi=200.)
    ax0 = plt.subplot(1,1,1)
    
    plot = ax0.bar(np.arange(len(AUC_mean)),
                   AUC_mean,
                   yerr = AUC_std,
                   error_kw = {"elinewidth" : 1,
                               "solid_capstyle" : "projecting",
                               "capsize" : 5,
                               "capthick" : 1,
                               },
                   color = ["#81dafc", "#ff6961"],
                   edgecolor = "black",
                   linewidth = 1.,
                   alpha = 0.8,
                   # zorder = 1,
                   )
    
    scat = sns.swarmplot(np.concatenate([np.full_like(all_AUC1, 0), np.full_like(all_AUC2, 1)]),
                         np.concatenate([all_AUC1, all_AUC2]),
                         ax=ax0,
                         s=10,
                         palette=["#81dafc", "#ff6961"],
                         edgecolor = "black",
                         linewidth = 1.,
                         alpha=0.8,
                         # zorder = 0,
                         )
    
    y_max = max([max(all_AUC1), max(all_AUC2)]) + max([max(all_AUC1), max(all_AUC2)])*0.1
    y_min = min([min(all_AUC1), min(all_AUC2)]) + min([min(all_AUC1), min(all_AUC2)])*0.1
    ax0.plot((0,0), (y_max+y_max*0.05, y_max+y_max*0.1), lw=1, color="black")
    ax0.plot((1,1), (y_max+y_max*0.05, y_max+y_max*0.1), lw=1, color="black")
    ax0.plot((0,1), (y_max+y_max*0.1, y_max+y_max*0.1), lw=1, color="black")
    
    ut.print_in_color("The comparison of AUC for before and after the behavioral initiation is : {0}".format(pval), "GREEN")
    
    if pval > 0.05 and pval >= 0.01 :
        
        ax0.text(0.5, y_max+y_max*0.1, "n.s")
    
    elif pval <= 0.05 and pval > 0.01 :
        
        ax0.text(0.5, y_max+y_max*0.1, "*")
        
    elif pval <= 0.01 and pval > 0.001 :
        
        ax0.text(0.5, y_max+y_max*0.1, "**")
        
    elif pval <= 0.001 and pval > 0.0001 :
        
        ax0.text(0.5, y_max+y_max*0.1, "***")
        
    elif pval <= 0.0001 :
        
        ax0.text(0.5, y_max+y_max*0.1, "****")
    
    ax0.set_yticks(np.arange(round(y_min), round(y_max+y_max*0.3)+2, 1))
    ax0.set_yticklabels(np.arange(round(y_min), round(y_max+y_max*0.3)+2, 1),  fontsize=kwargs["fsl"])
    ax0.plot((-0.5, 1.5), (0, 0), lw=1, color="black")
    ax0.set_xticks([0, 1])
    ax0.set_xticklabels(["Before initiating {0}".format(kwargs["behavior_to_segment"]),"After initiating {0}".format(kwargs["behavior_to_segment"])], fontsize=kwargs["fsl"])
    
    ax0.set_ylim(y_min+y_min*0.5, y_max+y_max*0.5)
    ax0.set_ylabel("Area under the curve (AUC)", fontsize=kwargs["fsl"])
    ax0.set_title("Before vs After initiation of {0} Response Changes".format(kwargs["behavior_to_segment"]), fontsize=kwargs["fst"])
    
    fig.tight_layout()
    
    if kwargs["save"] :
        
        plt.savefig(os.path.join(kwargs["save_dir"], "AUC.{0}".format(kwargs["extension"])), dpi=200., bbox_inches='tight')
        
    
    
    