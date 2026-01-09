xref_lookup = load('xref_lookup.mat');
disp(xref_lookup);

% from an cell containing cells i want to get an array
cpArray = cell2mat(xref_lookup.cp_vector);
ctArray = cell2mat(xref_lookup.ct_vector);

% display the max cp from cp_vector and the ct value of the same index
[maxCp, idx] = max(cpArray);
ctValue = ctArray(idx);
fprintf('Max Cp: %.2f, Corresponding ct value: %.2f\n', maxCp, ctValue);
