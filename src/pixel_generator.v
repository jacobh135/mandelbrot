module pixel_generator (
    input wire signed [10:0] x_t, y_t,
    output reg [9:0] x_pos, y_pos
);
    reg signed [10:0] x_sum;
    reg signed [10:0] y_sum;

    always @(*) begin
        if ((x_t + 32 < 640) && (y_t < 480)) begin
            x_sum = x_t + 11'sd32;
            x_pos = {x_sum[9:5], 5'b00000};
            y_sum = y_t;
            y_pos = {y_sum[9:5], 5'b00000};
        end
        else begin
            x_pos = 0;
            if (y_t >= 479) begin
                y_sum = 0;
            end
            else begin
                y_sum = y_t + 1;
            end
            y_pos = {y_sum[9:5], 5'b00000};
        end
    end

endmodule