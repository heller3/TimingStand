#! /usr/bin/env python
import os, sys, shutil
import csv
from ROOT import *
from array import array
from collections import namedtuple

def process_file(outfile, run, x0, y0, chidx, ptkidx):

    rootfile = TFile(outfile, "UPDATE")
    if (rootfile.IsZombie() or not rootfile.IsOpen()):
        return 'ERROR: Could not recover TTree, please check file:', outfile
    pulse = rootfile.Get('pulse')


    this_chidx, this_ptkidx = [], []
    if 'VME' in outfile:
        this_chidx = [-1 if x>100 else x for x in chidx]
        this_ptkidx = [-1 if x>100 else x for x in ptkidx]
    elif 'DT5742' in outfile:
        this_chidx = [-1 if x<99 else x-100 for x in chidx]
        this_ptkidx = [-1 if x<99 else x-100 for x in ptkidx]

    arr_x0, arr_y0, arr_run = array('f',[x0]), array('f',[y0]), array('i',[run])
    arr_chidx = array('i', this_chidx)
    arr_ptkidx = array('i', this_ptkidx)

    b_x0 = pulse.Branch("x0",arr_x0,"x0/F")
    b_y0 = pulse.Branch("y0",arr_y0,"y0/F")
    b_run = pulse.Branch("run",arr_run,"run/I")
    b_chidx = pulse.Branch("chidx",arr_chidx,'chidx[{0}]/I'.format(len(chidx)))
    b_ptkidx = pulse.Branch("ptkidx",arr_ptkidx,'ptkidx[{0}]/I'.format(len(ptkidx)))

    for i in range(pulse.GetEntries()):
        b_x0.Fill()
        b_y0.Fill()
        b_run.Fill()
        b_chidx.Fill()
        b_ptkidx.Fill()
    
    pulse.Write()
    rootfile.Close()
    return '...done'

def read_config(dut_name, nchans):
    batch = namedtuple('batch', ['grl', 'x0', 'y0', 'bv', 'chidx', 'ptkidx'])
    batch_list = []
    with open(dut_name+'.csv') as csvfile:
        next(csvfile) # skip header row
        for line in csvfile:
            _grl = []
            _x0, _y0, _bv = -999, -999, -999
            _chidx, _ptkidx = [None]*nchans, [None]*nchans

            _vals = line.strip().split(',')
            # parse run list
            _tmp = [ent for ent in _vals[0].split(';') if ent!='']
            for irn in _tmp:
                if '-' in irn:
                    _grl.extend([x for x in range(int(irn.split('-')[0]), int(irn.split('-')[-1])+1)])
                else:
                    _grl.append(int(irn))

            if _vals[1]=='-': _x0 = batch_list[-1].x0
            else: _x0 = float(_vals[1])
            if _vals[2]=='-': _y0 = batch_list[-1].y0
            else: _y0 = float(_vals[2])
            if _vals[3]=='-': _bv = batch_list[-1].bv
            else: _bv = int(_vals[3])

            for ich in range(nchans):
                _idx = 4+2*ich
                if _vals[_idx]=='-': _chidx[ich] = batch_list[-1].chidx[ich]
                else: _chidx[ich] = int(_vals[_idx])
                if _vals[_idx+1]=='-': _ptkidx[ich] = batch_list[-1].ptkidx[ich]
                else: _ptkidx[ich] = int(_vals[_idx+1])
            
            batch_list.append(batch(_grl,_x0, _y0, _bv, _chidx, _ptkidx))

    if verbose:
        for ib in batch_list: 
            print ib.x0, ib.y0, ib.bv, ib.chidx, ib.ptkidx
    return batch_list

if __name__ == '__main__':
    
    dut_name = '2x2mm_2x8_W6'
    nchans = 16
    verbose = False

    vme_reco_dir = '/eos/uscms/store/group/cmstestbeam/BTL_ETL/2018_11/data/VME/RECO/v6/'
    vme_file = vme_reco_dir+'DataVMETiming_RunRN.root'

    dt_reco_dir = vme_reco_dir.replace('VME','DT5742')
    dt_file = dt_reco_dir+'DT5742_RunRN.root'

    batch_list = read_config(dut_name, nchans)

    for ib in batch_list:
        for run in ib.grl:
            for infile in [vme_file.replace('RN',str(run)), dt_file.replace('RN',str(run))]:
                if not os.path.exists(infile):
                    print 'File not found:', infile
                    continue
                outfile = infile.replace('.root','_{}_bv{}.root'.format(dut_name, ib.bv))
                if os.path.exists(outfile):
                    print 'File already exists:', outfile
                    continue
                shutil.copyfile(infile, outfile)
                print 'Processing file:', infile,
                print process_file(outfile, run, ib.x0, ib.y0, ib.chidx, ib.ptkidx)

    # run = 1660
    # infile = '/Users/ana/mtd/testbeam/data/VME/RECO/v6/DataVMETiming_RunRN.root'.replace('RN',str(run))
    # print 'Processing file:', infile,
    # outfile = infile.replace('.root','_{}_bv{}.root'.format(dut_name, 500))
    # shutil.copyfile(infile, outfile)
    # print process_file(outfile, run, 10, 10.5, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
