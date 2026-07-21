module count_register (
    input wire capture, advance, clk, rst_n,
    input wire [4:0] count,
    output reg [4:0] active_count
);
    reg [4:0] stored_count;

    always @(posedge clk) begin
        if (~rst_n) begin
            active_count <= 0;
            stored_count <= 0;
        end
        else begin
            if (capture && advance) begin
                active_count <= count;
            end
            else begin
                if (capture) begin
                    stored_count <= count;
                end
                if (advance) begin
                    active_count <= stored_count;
                    stored_count <= 0;
                end
            end
        end
    end

endmodule