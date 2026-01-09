function table_value = table_look_up(table, row, column, row_value, column_value)

    column_index_under = 0;
    for i = 1:length(column) - 1
        if column_value > column(i)
            column_index_under = i;
        end
    end

    row_index_under = 0;
    for i = 1:length(row) - 1
        if row_value > row(i)
            row_index_under = i;
        end
    end

    if column_index_under == 0
        column_under_coef = 1;
        column_index_under = 1;
    elseif column_value > column(end)
        column_under_coef = 0;
    else
        column_under_coef = abs((column(column_index_under + 1) - column_value) / ...
                                (column(column_index_under) - column(column_index_under + 1)));
    end

    if row_index_under == 0
        row_under_coef = 1;
        row_index_under = 1;
    elseif row_value > row(end)
        row_under_coef = 0;
    else
        row_under_coef = abs((row(row_index_under + 1) - row_value) / ...
                             (row(row_index_under) - row(row_index_under + 1)));
    end

    table_value = table(row_index_under, column_index_under) * ...
                     (column_under_coef * row_under_coef) ...
                 + table(row_index_under + 1, column_index_under) * ...
                     ((1 - row_under_coef) * column_under_coef) ...
                 + table(row_index_under, column_index_under + 1) * ...
                     (row_under_coef * (1 - column_under_coef)) ...
                 + table(row_index_under + 1, column_index_under + 1) * ...
                     ((1 - row_under_coef) * (1 - column_under_coef));
end